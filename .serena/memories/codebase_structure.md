# Codebase Structure

## Directory Layout
```
myapp/
├── src/
│   ├── core/                    # Core framework modules
│   │   ├── asset_generator.py   # CSS/JS asset generation
│   │   ├── base_config.py       # Base configuration handling
│   │   ├── chart_generator.py   # Chart/visualization generation
│   │   ├── config.py           # Configuration management
│   │   ├── content_manager.py  # Content generation management
│   │   ├── document_builder.py # Markdown document building
│   │   ├── knowledge_manager.py # Knowledge base management
│   │   ├── mkdocs_manager.py   # MkDocs configuration
│   │   ├── platform_builder.py # Platform generation
│   │   ├── table_generator.py  # Table generation
│   │   └── utils.py           # Utility functions
│   ├── materials/              # Material implementations
│   │   └── test_material/      # Test material example
│   │       ├── content/        # YAML content files
│   │       ├── templates/      # Jinja2 templates
│   │       ├── contents.py     # Content manager implementation
│   │       └── main.py        # Material build script
│   └── learning_objects/       # Reusable learning components
├── tests/                      # Unit tests
│   └── core/                  # Core module tests
├── docs/                      # Generated documentation output
├── documents/                 # Project documentation
├── mkdocs.yml                 # MkDocs configuration
├── pyproject.toml            # Python project configuration
├── requirements.txt          # Python dependencies
├── pytest.ini               # pytest configuration
└── README.md                 # Project README
```

## Key Files
- `src/materials/test_material/main.py` - Main build script example
- `src/core/document_builder.py` - Core document generation class
- `src/core/mkdocs_manager.py` - MkDocs integration
- `content/*.yml` - YAML content configuration files