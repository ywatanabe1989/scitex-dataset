.PHONY: help install install-dev test lint lint-fix format clean run-examples

help:
	@echo "scitex-dataset - Unified access to neuroscience datasets"
	@echo ""
	@echo "Usage:"
	@echo "  make install       Install package"
	@echo "  make install-dev   Install package with dev dependencies"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linter"
	@echo "  make lint-fix      Run linter with auto-fix"
	@echo "  make format        Format code"
	@echo "  make clean         Clean build artifacts"
	@echo "  make run-examples  Run all examples"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,mcp]"

test:
	pytest tests/ -v

lint:
	ruff check src/

lint-fix:
	ruff check src/ --fix

format:
	ruff format src/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run-examples:
	@./examples/00_run_all.sh
