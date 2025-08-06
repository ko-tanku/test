const path = require('path');
const fs = require('fs');

module.exports = function myDynamicPagesPlugin(context, options) {
  return {
    name: 'practical-demo-plugin',

    async loadContent() {
      // Pythonスクリプトが生成したJSONデータを読み込む
      const dataPath = path.join(context.siteDir, 'static', 'data', 'practical-demo-pages.json');
      const rawData = fs.readFileSync(dataPath, 'utf-8');
      const data = JSON.parse(rawData);
      return data;
    },

    async contentLoaded({ content, actions }) {
      const { addRoute } = actions;

      content.forEach(pageData => {
        addRoute({
          path: `/practical-demo/${pageData.id}`,
          component: '@site/src/components/ComprehensiveTestPage.js',
          props: { pageData },
          exact: true,
        });
      });
    },
  };
};