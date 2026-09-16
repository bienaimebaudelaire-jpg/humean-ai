# Contributing to HUMEAN

Thank you for your interest in contributing to HUMEAN! This document provides guidelines and instructions.

## Getting Started

### Prerequisites
- Python 3.10+
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/bienaimebaudelaire-jpg/humean-ai.git
cd humean-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Setup pre-commit hooks
pre-commit install
```

## Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes
- Write clean, well-documented code
- Follow PEP 8 style guidelines
- Add type hints where possible

### 3. Run Tests Locally
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=modules

# Run specific test
pytest tests/test_config.py
```

### 4. Format Code
```bash
# Format code with black
black modules tests

# Check with ruff
ruff check modules tests
```

### 5. Commit & Push
```bash
git add .
git commit -m "feat: Add new feature" -m "Description of changes"
git push origin feature/your-feature-name
```

### 6. Create Pull Request
- Fill in the PR template
- Reference related issues
- Ensure all CI checks pass

## Code Standards

### Type Hints
Always use type hints for function arguments and return values:
```python
def process_data(input_text: str, threshold: float) -> dict[str, Any]:
    """Process input data and return results."""
    pass
```

### Docstrings
Use Google-style docstrings:
```python
def function_name(arg1: str, arg2: int) -> bool:
    """Brief description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value
    """
    pass
```

### Testing
- Write tests for new features
- Maintain >80% code coverage
- Test edge cases and error conditions

## Commit Message Guidelines

Format: `<type>(<scope>): <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Build, dependencies, tooling

Example:
```
feat(cognitive-engine): Add retry logic for API fallbacks
docs(README): Update installation instructions
```

## Questions?

- Open an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Use descriptive titles and detailed descriptions

Happy coding! 🚀
