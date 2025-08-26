# Code Style and Conventions

## Python Code Style
Based on the examined code, this project follows these conventions:

### Type Hints
- All function parameters and return types use type hints
- `pathlib.Path` is used for file paths instead of strings
- Complex types are properly annotated

### Documentation
- **Docstrings**: All classes and methods have Japanese docstrings
- **Format**: Uses standard Python docstring format with Args/Raises sections
- **Language**: Docstrings are written in Japanese
- **Comments**: Code comments also in Japanese

### Naming Conventions
- **Classes**: PascalCase (e.g., `DocumentBuilder`, `MkDocsManager`)
- **Functions/Methods**: snake_case (e.g., `add_heading`, `generate_content`)
- **Variables**: snake_case (e.g., `output_dir`, `content_buffer`)
- **Constants**: UPPER_SNAKE_CASE
- **Private methods**: Prefixed with underscore (e.g., `_escape_js_string`)

### Code Organization
- One class per file when possible
- Related functions grouped in modules
- Clear separation between core framework and material implementations
- Use of `__init__.py` files for proper package structure

### Error Handling
- Uses `raise ValueError()` with descriptive Japanese error messages
- Validates input parameters (e.g., heading levels 1-6)
- Proper exception handling in file operations

### Import Style
- Standard library imports first
- Third-party imports second
- Local imports last
- Uses `from pathlib import Path` pattern

### Method Structure
- Clear parameter validation
- Descriptive error messages
- Consistent return patterns
- Buffer-based content building pattern