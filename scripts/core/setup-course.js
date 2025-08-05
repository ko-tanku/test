// @ts-check
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const t = require('@babel/types');
const recast = require('recast');

// --- Configuration ---
const PROJECT_ROOT = path.resolve(__dirname, '..', '..');
const CONFIG_FILE = path.join(PROJECT_ROOT, 'docusaurus.config.js');
const COURSES_DIR = path.join(PROJECT_ROOT, 'scripts', 'courses');

/**
 * Main function to set up the course.
 * @param {string} courseId
 */
function main(courseId) {
  console.log(`--- Setting up course: ${courseId} ---`);

  // 1. Load course metadata
  const masterFile = path.join(COURSES_DIR, courseId, 'master.yaml');
  console.log(`Attempting to load master.yaml from: ${masterFile}`); // 追加
  if (!fs.existsSync(masterFile)) {
    console.error(`Error: master.yaml not found for course '${courseId}'`);
    process.exit(1);
  }
  const masterData = yaml.load(fs.readFileSync(masterFile, 'utf8'));
  const courseLabel = masterData.course_label;
  if (!courseLabel) {
    console.error(`Error: 'course_label' not found in ${masterFile}`);
    process.exit(1);
  }

  // 2. Parse the docusaurus.config.js file using recast to preserve formatting
  console.log(`Parsing ${CONFIG_FILE}...`);
  const code = fs.readFileSync(CONFIG_FILE, 'utf-8');
  const ast = recast.parse(code, {
    parser: {
      parse: (source) => parser.parse(source, { sourceType: 'module' }),
    },
  });
  console.log('AST parsed successfully.');
  // DEBUG: Log the AST structure
  // console.log(JSON.stringify(ast.program.body, null, 2));

  // 3. Find the main config object
  let configObject = null;
  traverse(ast, {
    VariableDeclarator(path) {
      if (path.node.id.type === 'Identifier' && path.node.id.name === 'config') {
        configObject = path.node.init;
        path.stop(); // Stop traversal once found
      }
    }
  });

  if (!configObject || configObject.type !== 'ObjectExpression') {
    console.error('Could not find the config ObjectExpression in docusaurus.config.js');
    process.exit(1);
  }

  // --- Modify plugins array ---
  const pluginsProp = configObject.properties.find(p => p.key.name === 'plugins');
  if (!pluginsProp || pluginsProp.value.type !== 'ArrayExpression') {
    console.error('Could not find a valid \'plugins\' array.');
    process.exit(1);
  }
  const pluginsArray = pluginsProp.value.elements;
  console.log(`Existing plugins elements count: ${pluginsArray.length}`);

  // Filter out all existing plugins related to this courseId
  const filteredPlugins = pluginsArray.filter(elem => {
    // Check for standard @docusaurus/plugin-content-docs
    if (t.isArrayExpression(elem) && elem.elements.length > 1 && t.isStringLiteral(elem.elements[0], { value: '@docusaurus/plugin-content-docs' })) {
      const configObject = elem.elements[1];
      if (t.isObjectExpression(configObject)) {
        const idProp = configObject.properties.find(p => t.isIdentifier(p.key, { name: 'id' }));
        if (idProp && t.isStringLiteral(idProp.value, { value: courseId })) {
          console.log(`Removing standard plugin for ${courseId}`);
          return false; // Remove this standard plugin
        }
      }
    }
    // Check for custom plugin path.resolve(__dirname, 'plugins', '[course_id]-plugin')
    if (t.isCallExpression(elem) && t.isMemberExpression(elem.callee) && t.isIdentifier(elem.callee.property, { name: 'resolve' })) {
      const args = elem.arguments;
      if (args.length > 1 && t.isStringLiteral(args[args.length - 1]) && args[args.length - 1].value.includes(`plugins/${courseId}-plugin`)) {
        console.log(`Removing custom plugin for ${courseId}`);
        return false; // Remove this custom plugin
      }
    }
    return true; // Keep other plugins
  });

  // Add the new custom plugin
  const pluginPath = `plugins/${courseId}-plugin`;
  const newPluginCode = `path.resolve(__dirname, '${pluginPath}')`;
  const newPluginAst = parser.parseExpression(newPluginCode);
  filteredPlugins.push(newPluginAst);
  
  pluginsProp.value.elements = filteredPlugins; // Replace the elements array
  console.log(`Updated plugins array for '${courseId}'. New count: ${filteredPlugins.length}`);

  // --- Modify navbar.items array ---
  const themeConfigProp = configObject.properties.find(p => p.key.name === 'themeConfig');
  const navbarProp = themeConfigProp && themeConfigProp.value.properties.find(p => p.key.name === 'navbar');
  const itemsProp = navbarProp && navbarProp.value.properties.find(p => p.key.name === 'items');
  if (!itemsProp || itemsProp.value.type !== 'ArrayExpression') {
    console.error('Could not find a valid \'navbar.items\' array.');
    process.exit(1);
  }
  const itemsArray = itemsProp.value.elements;
  console.log(`Existing navbar items count: ${itemsArray.length}`);

  const newItems = itemsArray.filter(elem => {
      if (elem.type !== 'ObjectExpression') return true;
      const idProp = elem.properties.find(p => p.key.name === 'docsPluginId');
      return !idProp || idProp.value.value !== courseId;
  });

  const newItem = t.objectExpression([
    t.objectProperty(t.identifier('type'), t.stringLiteral('docSidebar')),
    t.objectProperty(t.identifier('sidebarId'), t.stringLiteral(`${courseId}Sidebar`)),
    t.objectProperty(t.identifier('docsPluginId'), t.stringLiteral(courseId)),
    t.objectProperty(t.identifier('position'), t.stringLiteral('left')),
    t.objectProperty(t.identifier('label'), t.stringLiteral(courseLabel)),
  ]);
  newItems.push(newItem);

  itemsProp.value.elements = newItems; // Replace the elements array
  console.log(`Updated navbar.items array for '${courseId}'. New count: ${newItems.length}`);

  // 4. Generate the new code and write it back
  console.log(`Generating updated ${CONFIG_FILE}...`);
  const output = recast.print(ast, { tabWidth: 2, quote: 'single' });
  console.log('Generated code length:', output.code.length);
  fs.writeFileSync(CONFIG_FILE, output.code, 'utf-8');
  console.log('File written successfully.');

  console.log(`
--- Successfully set up course: ${courseId} ---
`);
}

if (require.main === module) {
  if (process.argv.length !== 3) {
    console.log("Usage: node scripts/core/setup-course.js [course_id]");
    process.exit(1);
  }
  main(process.argv[2]);
}
