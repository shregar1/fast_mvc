# CLI Reference

FastMVC provides an interactive CLI for project generation and management.

## Commands

### `fastmvc generate`

Interactive project generation wizard.

```bash
fastmvc generate [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--name` | Project name | Prompt |
| `--output` | Output directory | Current directory |
| `--author` | Author name | Git config or prompt |
| `--email` | Author email | Git config or prompt |
| `--description` | Project description | Prompt |
| `--venv / --no-venv` | Create virtual environment | `True` |
| `--venv-name` | Virtual environment name | `.venv` |
| `--install-deps / --no-install-deps` | Install dependencies | `True` |
| `--pre-commit / --no-pre-commit` | Install pre-commit hooks | `True` |
| `--non-interactive` | Skip interactive prompts | `False` |

**Examples:**

```bash
# Interactive mode
fastmvc generate

# With all options
fastmvc generate --name my-api --author "John Doe" --venv-name .venv

# Non-interactive
fastmvc generate --name my-api --non-interactive
```

### `fastmvc quickstart`

Quick project generation with defaults.

```bash
fastmvc quickstart <project_name> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `project_name` | Name of the project (required) |

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output directory | Current directory |
| `--venv-name` | Virtual environment name | `.venv` |
| `--no-venv` | Skip virtual environment creation | `False` |
| `--no-install` | Skip dependency installation | `False` |
| `--no-pre-commit` | Skip pre-commit setup | `False` |

**Examples:**

```bash
# Quick start with defaults
fastmvc quickstart my-project

# With custom options
fastmvc quickstart my-project --venv-name env --no-pre-commit
```

### `fastmvc --version`

Show version information.

```bash
fastmvc --version
```

## Makefile Commands

Generated projects include a `Makefile` with common development tasks:

### Setup

```bash
make install          # Install dependencies and setup project
make venv             # Create virtual environment only
make install-dev      # Install development dependencies
```

### Development

```bash
make dev              # Run with hot reload (default)
make dev-no-reload    # Run without reload
make prod             # Run production server (4 workers)
```

### Testing

```bash
make test             # Run tests
make test-verbose     # Run with verbose output
make test-coverage    # Run with coverage report
make test-watch       # Run continuously on file changes
```

### Code Quality

```bash
make lint             # Run linter
make lint-fix         # Run linter with auto-fix
make format           # Format code
make lint-format      # Run linter and format
make type-check       # Run type checking
make check            # Run all checks (lint + test)
make ci               # Run CI pipeline locally
```

### Database (if using Alembic)

```bash
make migrate          # Create new migration (make migrate msg="description")
make migrate-empty    # Create empty migration
make upgrade          # Apply all pending migrations
make downgrade        # Rollback last migration
make downgrade-all    # Rollback all migrations
make db-reset         # Reset database
make db-status        # Show migration status
```

### Documentation

```bash
make docs-install     # Install documentation dependencies
make docs-serve       # Serve documentation locally
make docs-build       # Build static documentation
make docs-deploy      # Deploy to GitHub Pages
```

### Docker

```bash
make docker-build     # Build Docker image
make docker-up        # Start services with Docker Compose
make docker-down      # Stop Docker services
make docker-logs      # Show Docker logs
make docker-clean     # Remove containers and volumes
```

### Utilities

```bash
make clean            # Remove cache files and build artifacts
make clean-all        # Clean + remove virtual environment
make generate-secret  # Generate a secure secret key
make open             # Open API docs in browser
```

## Interactive Features

### Progress Bars

The CLI shows progress bars during:
- File copying
- Dependency installation
- Virtual environment creation

### Rich Terminal Output

- ASCII art banner
- Styled tables for configuration summary
- Color-coded success/error messages
- Panel-based information display

### Prompt Validation

- Project name validation (no spaces, valid Python identifier)
- Email format validation
- Path existence checks

## VS Code Integration

Generated projects include VS Code tasks for all Makefile commands. Press `Cmd+Shift+P` (or `Ctrl+Shift+P`) and type "Run Task" to see all available tasks.

### Keyboard Shortcuts

- `F5` - Start debugging
- `Ctrl+F5` - Run without debugging
- `Cmd+Shift+B` - Build tasks
- `Cmd+Shift+T` - Run tests
