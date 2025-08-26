# Suggested Commands

## Development Commands

### Testing
- `pytest` - Run all tests
- `pytest tests/core/` - Run core module tests only
- `pytest -v` - Run tests with verbose output

### Content Generation
- `python src/materials/test_material/main.py` - Generate test material content
- `mkdocs build` - Build the documentation site
- `mkdocs serve` - Start local development server for preview

### Project Management
- `python -m pip install -r requirements.txt` - Install dependencies
- `python -m pip install -e .` - Install project in development mode

### Windows System Commands
Since this is running on Windows, use these commands:
- `dir` - List directory contents (instead of `ls`)
- `cd` - Change directory
- `type` - Display file contents (instead of `cat`)
- `findstr` - Search in files (instead of `grep`)
- `where` - Find executable location (instead of `which`)

### Development Workflow
1. Make changes to source code
2. Run `pytest` to ensure tests pass
3. Generate content with material main scripts
4. Use `mkdocs serve` to preview changes
5. Use `mkdocs build` for production build

### File Operations
- Content files are in `src/materials/*/content/*.yml`
- Generated files go to `docs/` directory
- Templates are in `src/materials/*/templates/`