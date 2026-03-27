# FastMVC Makefile
# Convenience commands for development
# Usage: make <command>

.PHONY: help install dev test lint format migrate shell clean docker-build docker-up docker-down

# Default target when running just 'make'
.DEFAULT_GOAL := help

# Colors for terminal output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

# Python executable (detects virtual environment)
PYTHON := $(shell if [ -d ".venv" ]; then echo ".venv/bin/python"; else echo "python"; fi)
PIP := $(shell if [ -d ".venv" ]; then echo ".venv/bin/pip"; else echo "pip"; fi)
UVICORN := $(shell if [ -d ".venv" ]; then echo ".venv/bin/uvicorn"; else echo "uvicorn"; fi)
PYTEST := $(shell if [ -d ".venv" ]; then echo ".venv/bin/pytest"; else echo "pytest"; fi)
ALEMBIC := $(shell if [ -d ".venv" ]; then echo ".venv/bin/alembic"; else echo "alembic"; fi)
RUFF := $(shell if [ -d ".venv" ]; then echo ".venv/bin/ruff"; else echo "ruff"; fi)

# Project name from pyproject.toml or directory
PROJECT_NAME := $(shell basename $(CURDIR))

## help: Show this help message
help:
	@echo "$(BLUE)FastMVC Development Commands$(RESET)"
	@echo ""
	@grep -E '^##' $(MAKEFILE_LIST) | sed -e 's/## //g' | column -t -s ':'
	@echo ""
	@echo "$(YELLOW)Tips:$(RESET)"
	@echo "  • Run 'make install' first to set up the project"
	@echo "  • Use 'make dev' to start the development server"
	@echo "  • Press Ctrl+C to stop the server"

## install: Install dependencies and create virtual environment
install:
	@echo "$(BLUE)🚀 Setting up $(PROJECT_NAME)...$(RESET)"
	@if [ ! -d ".venv" ]; then \
		echo "$(YELLOW)Creating virtual environment...$(RESET)"; \
		python3 -m venv .venv; \
		echo "$(GREEN)✓ Virtual environment created$(RESET)"; \
	else \
		echo "$(GREEN)✓ Virtual environment already exists$(RESET)"; \
	fi
	@echo "$(YELLOW)Installing dependencies...$(RESET)"
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(RESET)"
	@if [ -f ".env.example" ] && [ ! -f ".env" ]; then \
		cp .env.example .env; \
		echo "$(GREEN)✓ Created .env from .env.example$(RESET)"; \
	fi
	@echo ""
	@echo "$(GREEN)🎉 Setup complete! Run 'make dev' to start the server.$(RESET)"

## install-dev: Install development dependencies
install-dev:
	@echo "$(BLUE)📦 Installing development dependencies...$(RESET)"
	@$(PIP) install -r requirements-dev.txt
	@echo "$(GREEN)✓ Development dependencies installed$(RESET)"

## dev: Run development server with hot reload
dev:
	@echo "$(BLUE)🚀 Starting FastAPI development server...$(RESET)"
	@echo "$(YELLOW)Server will be available at: http://localhost:8000$(RESET)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(RESET)"
	@echo ""
	$(UVICORN) app:app --host 0.0.0.0 --port 8000 --reload

## dev-no-reload: Run server without hot reload (for debugging)
dev-no-reload:
	@echo "$(BLUE)🚀 Starting FastAPI server (no reload)...$(RESET)"
	@$(UVICORN) app:app --host 0.0.0.0 --port 8000

## prod: Run production server (no reload, 4 workers)
prod:
	@echo "$(BLUE)🚀 Starting FastAPI production server...$(RESET)"
	@$(UVICORN) app:app --host 0.0.0.0 --port 8000 --workers 4

## test: Run all tests
test:
	@echo "$(BLUE)🧪 Running tests...$(RESET)"
	@$(PYTEST) -v --tb=short

## test-verbose: Run tests with verbose output
test-verbose:
	@echo "$(BLUE)🧪 Running tests (verbose)...$(RESET)"
	@$(PYTEST) -vv --tb=long --capture=no

## test-coverage: Run tests with coverage report
test-coverage:
	@echo "$(BLUE)🧪 Running tests with coverage...$(RESET)"
	@$(PYTEST) --cov=. --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/$(RESET)"

## test-watch: Run tests continuously on file changes
test-watch:
	@echo "$(BLUE)👁️  Watching for changes...$(RESET)"
	@$(PIP) install pytest-watch -q 2>/dev/null || true
	@ptw -- -v --tb=short

## lint: Run linter (ruff)
lint:
	@echo "$(BLUE)🔍 Running linter...$(RESET)"
	@$(RUFF) check .

## lint-fix: Run linter with auto-fix
lint-fix:
	@echo "$(BLUE)🔧 Running linter with auto-fix...$(RESET)"
	@$(RUFF) check --fix .

## format: Format code with ruff
format:
	@echo "$(BLUE)✨ Formatting code...$(RESET)"
	@$(RUFF) format .
	@echo "$(GREEN)✓ Code formatted$(RESET)"

## lint-format: Run linter (fix) and format
lint-format: lint-fix format
	@echo "$(GREEN)✓ Linting and formatting complete$(RESET)"

## type-check: Run type checking (if mypy is installed)
type-check:
	@echo "$(BLUE)🔍 Running type checks...$(RESET)"
	@if command -v $(PYTHON) -m mypy >/dev/null 2>&1; then \
		$(PYTHON) -m mypy . --ignore-missing-imports; \
	else \
		echo "$(YELLOW)⚠ mypy not installed. Run: $(PIP) install mypy$(RESET)"; \
	fi

## migrate: Create new migration (usage: make migrate msg="description")
migrate:
	@if [ -z "$(msg)" ]; then \
		echo "$(RED)❌ Please provide a migration message: make migrate msg='add users table'$(RESET)"; \
		exit 1; \
	fi
	@echo "$(BLUE)🗃️  Creating migration: $(msg)$(RESET)"
	@$(ALEMBIC) revision --autogenerate -m "$(msg)"

## migrate-empty: Create empty migration
migrate-empty:
	@echo "$(BLUE)🗃️  Creating empty migration$(RESET)"
	@$(ALEMBIC) revision -m "empty migration"

## upgrade: Apply all pending migrations
upgrade:
	@echo "$(BLUE)🗃️  Applying migrations...$(RESET)"
	@$(ALEMBIC) upgrade head
	@echo "$(GREEN)✓ Migrations applied$(RESET)"

## downgrade: Rollback last migration
downgrade:
	@echo "$(YELLOW)🗃️  Rolling back last migration...$(RESET)"
	@$(ALEMBIC) downgrade -1
	@echo "$(GREEN)✓ Migration rolled back$(RESET)"

## downgrade-all: Rollback all migrations
downgrade-all:
	@echo "$(RED)🗃️  Rolling back ALL migrations...$(RESET)"
	@$(ALEMBIC) downgrade base
	@echo "$(GREEN)✓ All migrations rolled back$(RESET)"

## db-reset: Reset database (rollback all + upgrade)
db-reset:
	@echo "$(RED)🗃️  Resetting database...$(RESET)"
	@$(ALEMBIC) downgrade base
	@$(ALEMBIC) upgrade head
	@echo "$(GREEN)✓ Database reset$(RESET)"

## db-status: Show current migration status
db-status:
	@echo "$(BLUE)🗃️  Migration status:$(RESET)"
	@$(ALEMBIC) current
	@$(ALEMBIC) history --verbose

## shell: Open Python shell with project context
shell:
	@echo "$(BLUE)🐍 Starting Python shell...$(RESET)"
	@$(PYTHON) -c "import sys; sys.path.insert(0, '.'); import app; print('Loaded app'); print('Available: app, FastAPI, etc.')"
	@$(PYTHON) -i -c "import sys; sys.path.insert(0, '.'); import app; print('\n=== FastMVC Shell ===\n'); print('Variables available:'); print('  app - FastAPI application')"

## clean: Remove Python cache files and build artifacts
clean:
	@echo "$(BLUE)🧹 Cleaning up...$(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✓ Cleanup complete$(RESET)"

## clean-all: Clean + remove virtual environment
clean-all: clean
	@echo "$(RED)🧹 Removing virtual environment...$(RESET)"
	@rm -rf .venv venv env ENV
	@echo "$(GREEN)✓ Virtual environment removed$(RESET)"

## docker-build: Build Docker image
docker-build:
	@echo "$(BLUE)🐳 Building Docker image...$(RESET)"
	@docker build -t $(PROJECT_NAME):latest .
	@echo "$(GREEN)✓ Docker image built: $(PROJECT_NAME):latest$(RESET)"

## docker-up: Start services with Docker Compose
docker-up:
	@echo "$(BLUE)🐳 Starting Docker services...$(RESET)"
	@docker-compose up -d
	@echo "$(GREEN)✓ Services started$(RESET)"
	@echo "$(YELLOW)API: http://localhost:8000$(RESET)"

## docker-down: Stop Docker services
docker-down:
	@echo "$(BLUE)🐳 Stopping Docker services...$(RESET)"
	@docker-compose down
	@echo "$(GREEN)✓ Services stopped$(RESET)"

## docker-logs: Show Docker logs
docker-logs:
	@docker-compose logs -f

## docker-clean: Remove Docker containers and volumes
docker-clean:
	@echo "$(RED)🐳 Removing Docker containers and volumes...$(RESET)"
	@docker-compose down -v --remove-orphans
	@docker rmi $(PROJECT_NAME):latest 2>/dev/null || true
	@echo "$(GREEN)✓ Docker cleanup complete$(RESET)"

## venv: Create virtual environment only
venv:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		echo "$(GREEN)✓ Virtual environment created at .venv/$(RESET)"; \
		echo "$(YELLOW)Activate with: source .venv/bin/activate$(RESET)"; \
	else \
		echo "$(GREEN)✓ Virtual environment already exists$(RESET)"; \
	fi

## check: Run all checks (lint, test)
check: lint test
	@echo "$(GREEN)✓ All checks passed$(RESET)"

## ci: Run CI pipeline locally (lint + test + coverage)
ci: lint format test-coverage
	@echo "$(GREEN)✓ CI checks complete$(RESET)"

## open: Open API documentation in browser (macOS/Linux)
open:
	@echo "$(BLUE)🌐 Opening API documentation...$(RESET)"
	@if command -v open >/dev/null 2>&1; then \
		open http://localhost:8000/docs; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open http://localhost:8000/docs; \
	else \
		echo "$(YELLOW)Please open: http://localhost:8000/docs$(RESET)"; \
	fi

# Secret key generation for .env
## generate-secret: Generate a secure secret key
generate-secret:
	@echo "$(BLUE)🔑 Generating secret key...$(RESET)"
	@$(PYTHON) -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# Documentation commands
## docs-install: Install documentation dependencies
docs-install:
	@echo "$(BLUE)📚 Installing documentation dependencies...$(RESET)"
	@$(PIP) install -r requirements-docs.txt
	@echo "$(GREEN)✓ Documentation dependencies installed$(RESET)"

## docs-serve: Serve documentation locally with hot reload
docs-serve:
	@echo "$(BLUE)📚 Starting documentation server...$(RESET)"
	@echo "$(YELLOW)Documentation will be available at: http://localhost:8001$(RESET)"
	@echo "$(YELLOW)Press Ctrl+C to stop$(RESET)"
	@$(PYTHON) -m mkdocs serve

## docs-build: Build static documentation
docs-build:
	@echo "$(BLUE)📚 Building documentation...$(RESET)"
	@$(PYTHON) -m mkdocs build
	@echo "$(GREEN)✓ Documentation built to site/$(RESET)"

## docs-deploy: Deploy documentation to GitHub Pages
docs-deploy:
	@echo "$(BLUE)📚 Deploying documentation...$(RESET)"
	@$(PYTHON) -m mkdocs gh-deploy --force
	@echo "$(GREEN)✓ Documentation deployed$(RESET)"
