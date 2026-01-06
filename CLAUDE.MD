# CLAUDE.MD - AI Assistant Context

This file provides comprehensive context about the Unifi MCP Server repository for AI assistants like Claude.

## Project Overview

**Name:** Unifi MCP Server
**Purpose:** A Model Context Protocol (MCP) server that integrates the UI.com Site Manager API with Claude Desktop
**Language:** Python 3.8+
**License:** MIT
**Status:** Production-ready (v1.0.0)

### What This Project Does

This is a production-quality MCP server that allows Claude Desktop users to interact with their UniFi network infrastructure using natural language. It provides 100% coverage of the UniFi Site Manager API v1.0, including:

- Host management (list, get details)
- Site management (list sites)
- Device management (list, filter)
- ISP metrics (performance data)
- SD-WAN configuration management

## Repository Structure

```
Unimcp/
├── src/unifi_mcp/           # Main package (proper Python package structure)
│   ├── __init__.py          # Package metadata and exports
│   ├── client.py            # UniFi API client (189 lines)
│   ├── models.py            # Pydantic models for MCP tools (152 lines)
│   ├── server.py            # FastAPI app and entry point (96 lines)
│   ├── tools.py             # MCP tool definitions (263 lines)
│   └── resources.py         # MCP resource definitions (71 lines)
│
├── tests/                   # Comprehensive test suite
│   ├── conftest.py          # Pytest fixtures and configuration
│   ├── unit/                # Unit tests (mocked dependencies)
│   │   ├── test_client.py   # Tests for UniFi API client
│   │   └── test_models.py   # Tests for Pydantic models
│   └── integration/         # Integration tests (full workflows)
│       └── test_api_integration.py
│
├── docs/                    # User documentation
│   ├── README.md            # Documentation index
│   ├── 1_overview_project.md
│   ├── 2_installation_setup.md
│   ├── 3_configuration_guide.md
│   ├── 4_usage_guide.md
│   ├── 5_api_reference.md
│   ├── 6_docker_deployment.md
│   ├── 7_troubleshooting_guide.md
│   └── 8_maintenance_updates.md
│
├── .github/                 # GitHub configuration
│   ├── workflows/           # CI/CD pipelines
│   │   ├── ci.yml           # Multi-platform testing
│   │   └── release.yml      # Automated releases
│   ├── ISSUE_TEMPLATE/      # Issue templates
│   └── dependabot.yml       # Dependency updates
│
├── pyproject.toml           # Modern Python packaging (PEP 518/621)
├── requirements.txt         # Pinned production dependencies
├── requirements-dev.txt     # Development dependencies
├── Makefile                 # Common development tasks
├── Dockerfile               # Multi-stage, secure Docker build
├── docker-compose.yml       # Docker Compose configuration
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .editorconfig            # Editor configuration
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
├── CODE_OF_CONDUCT.md       # Contributor Covenant
└── README.md                # Main documentation

# Legacy files (for backward compatibility)
├── main.py                  # Old monolithic file (730 lines) - DO NOT MODIFY
├── test_unifi_client.py     # Legacy test file
├── test_api_coverage.py     # Legacy test file
├── configure_claude.py      # Claude Desktop configuration helper
└── start_server.sh/bat      # Legacy startup scripts
```

## Architecture

### Package Structure (src/unifi_mcp/)

The codebase follows a clean, modular architecture:

1. **client.py** - UniFi API Client
   - `UnifiClient` class handles all HTTP communication
   - Async methods using `httpx`
   - Built-in error handling and logging
   - Supports pagination, filtering, and all API endpoints

2. **models.py** - Pydantic Models
   - Input/output models for all MCP tools
   - Type validation and serialization
   - Comprehensive field descriptions
   - Optional and required field handling

3. **server.py** - FastAPI Application
   - Main application entry point
   - Health check endpoint at `/health`
   - Startup event initializes UniFi client
   - Registers all tools and resources

4. **tools.py** - MCP Tool Definitions
   - 12 MCP tools covering all API endpoints
   - Host management (2 tools)
   - Site management (1 tool)
   - Device management (1 tool)
   - ISP metrics (2 tools)
   - SD-WAN management (3 tools)
   - Legacy backward compatibility (3 tools)

5. **resources.py** - MCP Resource Definitions
   - 4 MCP resources for direct data access
   - Resources: hosts, sites, devices, sdwan-configs
   - URI scheme: `unifi://resource-name`

### Key Design Decisions

1. **Modular Architecture**: Split from 730-line monolith into focused modules
2. **Async-First**: All API calls use async/await for performance
3. **Type Safety**: Comprehensive type hints and Pydantic validation
4. **Error Handling**: HTTPException with detailed error messages
5. **Logging**: Structured logging throughout
6. **Backward Compatibility**: Legacy methods maintained for existing users

## Code Conventions

### Style Guide

- **Formatter**: Black (line length: 100)
- **Linter**: Ruff (strict rules enabled)
- **Type Checker**: MyPy (strict mode)
- **Import Order**: isort via Ruff

### Naming Conventions

- **Files**: lowercase with underscores (snake_case)
- **Classes**: PascalCase (e.g., `UnifiClient`, `ListHostsInput`)
- **Functions**: snake_case (e.g., `list_hosts`, `get_host_by_id`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `UNIFI_API_KEY`)
- **Private methods**: Leading underscore (e.g., `_make_request`)

### Type Hints

All functions should have complete type hints:

```python
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
async def get_host_by_id(self, host_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific host by ID.

    Args:
        host_id: Unique identifier of the host

    Returns:
        Dictionary containing host details from the API

    Raises:
        HTTPException: If the API request fails
    """
```

## Testing Strategy

### Test Organization

- **Unit Tests** (`tests/unit/`): Test individual components in isolation
  - Mock all external dependencies (httpx, environment variables)
  - Test all code paths including error cases
  - Fast execution (<1 second total)

- **Integration Tests** (`tests/integration/`): Test full workflows
  - Test multiple components working together
  - Use realistic data flows
  - Test pagination, filtering, etc.

### Running Tests

```bash
# Run all tests with coverage
make test

# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run specific test file
pytest tests/unit/test_client.py -v

# Run with coverage report
pytest --cov --cov-report=html
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.asyncio` - Async tests (auto-applied)

### Fixtures

Common fixtures in `tests/conftest.py`:
- `mock_env`: Mocked environment variables
- `unifi_client`: Configured UnifiClient instance
- `sample_host_data`: Sample API response data
- `sample_site_data`: Sample site data
- `sample_device_data`: Sample device data
- `mock_httpx_response`: Mock HTTP responses

## Development Workflow

### Setup

```bash
# Clone and install
git clone https://github.com/djimit/Unimcp.git
cd Unimcp
make install-dev

# Or manually
pip install -e ".[dev]"
pre-commit install
```

### Common Tasks

```bash
make help          # Show all available commands
make format        # Format code (black + ruff)
make lint          # Run linters
make type-check    # Run MyPy
make test          # Run tests with coverage
make clean         # Remove build artifacts
make build         # Build Python package
make run           # Run the server locally
```

### Git Workflow

1. Create feature branch: `git checkout -b feature/name`
2. Make changes
3. Run quality checks: `make format lint type-check test`
4. Commit with conventional commits: `feat:`, `fix:`, `docs:`, etc.
5. Push and create PR

### Pre-commit Hooks

Automatically run on `git commit`:
- Trailing whitespace removal
- End-of-file fixer
- YAML/JSON/TOML validation
- Black formatting
- Ruff linting
- MyPy type checking

## Environment Variables

### Required

- `UNIFI_API_KEY`: UniFi Site Manager API key (required)

### Optional

- `UNIFI_API_URL`: API base URL (default: `https://api.ui.com`)

### Setting Up

```bash
cp .env.example .env
# Edit .env and add your API key
```

## Important Files to Know

### Configuration Files

- **pyproject.toml**: Single source of truth for package metadata, dependencies, and tool configurations
- **requirements.txt**: Pinned production dependencies
- **requirements-dev.txt**: Development dependencies
- **.pre-commit-config.yaml**: Pre-commit hook definitions
- **.editorconfig**: Cross-editor formatting rules

### Entry Points

- **src/unifi_mcp/server.py**: Main application (`python -m unifi_mcp.server`)
- **CLI command**: `unifi-mcp` (defined in pyproject.toml)
- **Legacy**: `main.py` (DO NOT MODIFY - kept for backward compatibility)

### CI/CD

- **.github/workflows/ci.yml**: Runs on push/PR - tests across Python 3.8-3.12, Ubuntu/Windows/macOS
- **.github/workflows/release.yml**: Runs on version tags - publishes to PyPI and Docker Hub
- **.github/dependabot.yml**: Weekly dependency updates

## API Coverage

This implementation provides **100% coverage** of the UI.com Site Manager API v1.0:

| Endpoint | Method | Tool Name |
|----------|--------|-----------|
| `/v1/hosts` | GET | `list_hosts` |
| `/v1/hosts/{hostId}` | GET | `get_host_by_id` |
| `/v1/sites` | GET | `list_sites` |
| `/v1/devices` | GET | `list_devices` |
| `/ea/isp-metrics/{type}` | GET | `get_isp_metrics` |
| `/ea/isp-metrics/query` | POST | `query_isp_metrics` |
| `/v1/sd-wan/configs` | GET | `list_sdwan_configs` |
| `/v1/sd-wan/configs/{configId}` | GET | `get_sdwan_config_by_id` |
| `/v1/sd-wan/configs/{configId}/status` | GET | `get_sdwan_config_status` |

## Common Tasks for AI Assistants

### Adding a New API Endpoint

1. Add method to `UnifiClient` in `src/unifi_mcp/client.py`
2. Create input/output models in `src/unifi_mcp/models.py`
3. Register tool in `src/unifi_mcp/tools.py`
4. Add unit tests in `tests/unit/test_client.py`
5. Add integration test in `tests/integration/`
6. Update API coverage table in README.md

### Fixing a Bug

1. Write a failing test that reproduces the bug
2. Fix the bug in the relevant module
3. Ensure all tests pass
4. Run quality checks: `make format lint type-check test`
5. Commit with `fix:` prefix

### Updating Dependencies

1. Edit `requirements.txt` or `requirements-dev.txt`
2. Test: `pip install -r requirements.txt && make test`
3. Update pyproject.toml if needed
4. Dependabot will also create automated PRs weekly

### Adding Documentation

1. Update relevant files in `docs/`
2. Update README.md if user-facing
3. Add docstrings to code
4. Update CLAUDE.MD (this file) if architecture changes

## Gotchas and Important Notes

### ⚠️ Critical Points

1. **DO NOT MODIFY main.py**: Legacy file kept for backward compatibility. All new code goes in `src/unifi_mcp/`

2. **Always use async/await**: The codebase is async-first. Use `async def` for new functions.

3. **MCP Dependency**: The `mcp` package may not be available. There's a fallback class in `server.py` - do not remove it.

4. **Environment Variables**: Tests use `mock_env` fixture. Always mock `UNIFI_API_KEY` in tests.

5. **Type Hints**: Required for all public functions. MyPy will fail without them.

6. **API Key Security**: Never commit API keys. They should only be in `.env` (which is gitignored).

### 🔧 Technical Details

1. **HTTP Client**: Uses `httpx` for async HTTP requests (not `requests`)

2. **Model Validation**: Pydantic v2 is used. Some syntax differs from v1.

3. **FastAPI Integration**: The MCP server is built on FastAPI, providing REST endpoints.

4. **Docker**: Multi-stage build with non-root user. Don't run as root.

5. **Python Versions**: Support 3.8-3.12. Test on all versions via CI.

### 🎯 Best Practices

1. **Small PRs**: Keep changes focused and reviewable
2. **Test Coverage**: Maintain >80% coverage
3. **Type Safety**: Use type hints everywhere
4. **Error Messages**: Provide helpful, actionable error messages
5. **Logging**: Log important events at appropriate levels
6. **Documentation**: Update docs when behavior changes

## Deployment

### Local Development

```bash
python -m unifi_mcp.server
# Or: unifi-mcp
# Or: make run
```

### Docker

```bash
docker build -t unifi-mcp-server .
docker run -p 8000:8000 -e UNIFI_API_KEY=your_key unifi-mcp-server

# Or: docker-compose up
```

### Production (Claude Desktop)

Add to Claude Desktop config:

```json
{
  "mcpServers": {
    "unifi": {
      "command": "unifi-mcp",
      "env": {
        "UNIFI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Recent Major Changes

### v1.0.0 Refactoring (January 2025)

The repository underwent a major quality improvement:

1. ✅ **Package Structure**: Split 730-line `main.py` into modular package
2. ✅ **Testing**: Added 50+ unit and integration tests with pytest
3. ✅ **CI/CD**: Implemented GitHub Actions for testing and releases
4. ✅ **Code Quality**: Added Black, Ruff, MyPy, and pre-commit hooks
5. ✅ **Documentation**: Added LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md
6. ✅ **Docker**: Enhanced with multi-stage builds and security
7. ✅ **Dependencies**: Pinned all versions for reproducible builds

**Migration Note**: Users should migrate from `python main.py` to `python -m unifi_mcp.server` or `unifi-mcp`.

## Troubleshooting

### Common Issues

1. **Import Errors**: Run `pip install -e ".[dev]"` to install in development mode
2. **Test Failures**: Check environment variables are mocked in fixtures
3. **Type Errors**: Run `make type-check` to see specific issues
4. **Formatting Issues**: Run `make format` to auto-fix
5. **Docker Build Fails**: Ensure you have the latest Dockerfile changes

### Getting Help

- Check `docs/7_troubleshooting_guide.md`
- Search existing issues on GitHub
- Review test files for examples
- Check CI logs for failed builds

## Links and Resources

- **Repository**: https://github.com/djimit/Unimcp
- **Issues**: https://github.com/djimit/Unimcp/issues
- **UniFi API Docs**: https://developer.ui.com/site-manager-api/
- **MCP Spec**: https://modelcontextprotocol.io/
- **Claude Desktop**: https://claude.ai/desktop

## Version History

- **v1.0.0** (January 2025): Major refactoring, production-ready release
- **v0.x**: Initial development, monolithic structure

---

**Last Updated**: January 2025
**Maintained By**: @djimit and contributors
**AI Assistant**: Feel free to reference this document when working with the codebase. It's kept up-to-date with architectural changes.
