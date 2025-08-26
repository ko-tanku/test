# Task Completion Checklist

## When Completing Development Tasks

### Code Quality
- [ ] Run `pytest` to ensure all tests pass
- [ ] Check that new functions have proper Japanese docstrings
- [ ] Verify type hints are properly added
- [ ] Ensure proper error handling with Japanese error messages

### Content Generation
- [ ] Test content generation by running the material's main script
- [ ] Verify generated Markdown is properly formatted
- [ ] Check that MkDocs builds without errors using `mkdocs build`
- [ ] Preview changes using `mkdocs serve`

### File Organization
- [ ] Ensure new files follow the established directory structure
- [ ] Add proper `__init__.py` files if creating new packages
- [ ] Place tests in appropriate `tests/` subdirectories
- [ ] Follow naming conventions (snake_case for files, PascalCase for classes)

### Documentation
- [ ] Update relevant YAML configuration files if needed
- [ ] Ensure any new features are reflected in content templates
- [ ] Verify Japanese text displays correctly in generated output

### Final Verification
- [ ] All imports are properly organized
- [ ] No unused imports or variables
- [ ] Code follows the established Japanese documentation pattern
- [ ] Generated content displays correctly in browser via `mkdocs serve`

## Common Issues to Check
- Path handling uses `pathlib.Path` instead of string concatenation
- YAML files use proper UTF-8 encoding for Japanese characters
- Template files have correct Jinja2 syntax
- Generated HTML is properly escaped