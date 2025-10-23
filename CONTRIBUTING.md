# Contributing to Unifi MCP Server

Thank you for your interest in contributing to the Unifi MCP Server! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct (see CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Unimcp.git
   cd Unimcp
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   make install-dev
   # Or manually:
   pip install -e ".[dev]"
   ```

4. **Set up pre-commit hooks**
   ```bash
   pre-commit install
   ```

## Development Workflow

### Creating a Branch

Create a new branch for your feature or bugfix:

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### Making Changes

1. **Write clean, documented code**
   - Follow PEP 8 style guidelines
   - Add docstrings to all functions and classes
   - Use type hints where appropriate
   - Keep functions small and focused

2. **Format your code**
   ```bash
   make format
   ```

3. **Run linters**
   ```bash
   make lint
   ```

4. **Run type checking**
   ```bash
   make type-check
   ```

### Testing

All contributions must include appropriate tests:

1. **Write tests for new functionality**
   - Unit tests in `tests/unit/`
   - Integration tests in `tests/integration/`

2. **Run tests**
   ```bash
   make test
   ```

3. **Check coverage**
   ```bash
   pytest --cov --cov-report=html
   # Open htmlcov/index.html in your browser
   ```

4. **Ensure all tests pass**
   - All existing tests must pass
   - New tests must be included for new features
   - Aim for >80% code coverage

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Maintenance tasks

Examples:
```
feat(client): Add support for SD-WAN status endpoint

Add new method to retrieve SD-WAN configuration status.
Includes unit tests and documentation updates.

Closes #123
```

```
fix(server): Handle connection timeout errors

Add proper error handling for network timeout scenarios.
Improves user experience with better error messages.
```

### Submitting a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template completely

3. **PR Checklist**
   - [ ] Code follows project style guidelines
   - [ ] All tests pass
   - [ ] New tests added for new functionality
   - [ ] Documentation updated
   - [ ] Commit messages follow conventions
   - [ ] No merge conflicts
   - [ ] PR description is clear and complete

4. **Wait for review**
   - Maintainers will review your PR
   - Address any feedback or requested changes
   - Keep the PR updated with the main branch

## Project Structure

```
Unimcp/
├── src/
│   └── unifi_mcp/
│       ├── __init__.py       # Package initialization
│       ├── client.py         # UniFi API client
│       ├── models.py         # Pydantic models
│       ├── server.py         # FastAPI server
│       ├── tools.py          # MCP tool definitions
│       └── resources.py      # MCP resource definitions
├── tests/
│   ├── unit/                 # Unit tests
│   │   ├── test_client.py
│   │   └── test_models.py
│   ├── integration/          # Integration tests
│   └── conftest.py           # Pytest fixtures
├── docs/                     # Documentation
├── .github/                  # GitHub configuration
│   ├── workflows/            # CI/CD workflows
│   └── ISSUE_TEMPLATE/       # Issue templates
├── pyproject.toml            # Project configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
└── Makefile                  # Development commands
```

## Code Style

### Python Code

We use the following tools to maintain code quality:

- **Black**: Code formatting (line length: 100)
- **Ruff**: Fast Python linter
- **MyPy**: Static type checking

These are enforced by pre-commit hooks and CI/CD.

### Type Hints

Use type hints for all function parameters and return values:

```python
from typing import Dict, List, Optional

async def list_hosts(
    self,
    page_size: Optional[int] = None,
    next_token: Optional[str] = None
) -> Dict[str, Any]:
    """Get list of all hosts."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of the function.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param2 is negative
    """
    ...
```

## Testing Guidelines

### Unit Tests

- Test individual functions and methods in isolation
- Use mocks for external dependencies
- Each test should test one thing
- Use descriptive test names

```python
@pytest.mark.unit
async def test_list_hosts_with_pagination(unifi_client, mock_httpx_response):
    """Test hosts listing with pagination parameters"""
    # Test implementation
```

### Integration Tests

- Test complete workflows
- Test interactions between components
- Use realistic data

```python
@pytest.mark.integration
async def test_full_host_workflow(mock_env, sample_host_data):
    """Test full workflow: list hosts -> get specific host"""
    # Test implementation
```

## Documentation

### Code Documentation

- Add docstrings to all public functions, classes, and methods
- Include examples in docstrings where helpful
- Document parameters, return values, and exceptions

### User Documentation

- Update relevant documentation files in `docs/`
- Add examples for new features
- Update README.md if needed

## Questions or Issues?

- Check existing [issues](https://github.com/djimit/Unimcp/issues)
- Open a new issue if your question hasn't been asked
- Join discussions in the repository

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
