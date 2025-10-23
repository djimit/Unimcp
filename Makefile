.PHONY: help install install-dev test test-unit test-integration lint format type-check clean build run docker-build docker-run pre-commit

help:
	@echo "Available targets:"
	@echo "  install         - Install production dependencies"
	@echo "  install-dev     - Install development dependencies"
	@echo "  test            - Run all tests with coverage"
	@echo "  test-unit       - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  lint            - Run ruff linter"
	@echo "  format          - Format code with black and ruff"
	@echo "  type-check      - Run mypy type checking"
	@echo "  clean           - Remove build artifacts and cache files"
	@echo "  build           - Build Python package"
	@echo "  run             - Run the MCP server"
	@echo "  docker-build    - Build Docker image"
	@echo "  docker-run      - Run Docker container"
	@echo "  pre-commit      - Install pre-commit hooks"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest -v --cov

test-unit:
	pytest -v -m unit --cov

test-integration:
	pytest -v -m integration --cov

lint:
	ruff check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

type-check:
	mypy src/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov dist build .mypy_cache .ruff_cache

build:
	python -m build

run:
	python -m unifi_mcp.server

docker-build:
	docker build -t unifi-mcp-server:latest .

docker-run:
	docker-compose up -d

pre-commit:
	pre-commit install
	pre-commit run --all-files
