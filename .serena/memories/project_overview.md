# Project Overview

## Purpose
This is a Japanese learning materials generator built with Python and MkDocs. The system automatically generates educational content and documentation using YAML configuration files and Python templates.

## Key Features
- Generates MkDocs-based learning materials
- Supports interactive content like quizzes, exercises, and charts
- Generates content from YAML configuration files
- Creates themed CSS and JavaScript assets
- Supports multiple material types and content structures
- Japanese language support throughout

## Tech Stack
- **Language**: Python 3.11+
- **Documentation**: MkDocs
- **Content Format**: Markdown with YAML configuration
- **Testing**: pytest
- **Template Engine**: Jinja2 templates
- **File Processing**: pathlib for path management
- **Content Types**: Learning objects, exercises, quizzes, glossaries, FAQ

## Main Components
- **Core Framework**: Located in `src/core/` - contains the main generation engines
- **Materials**: Located in `src/materials/` - specific material implementations
- **Learning Objects**: Located in `src/learning_objects/` - reusable content components
- **Tests**: Located in `tests/` - unit tests for core functionality
- **Documentation**: Located in `docs/` - generated output directory