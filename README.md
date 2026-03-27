# pyfastmvc

**Production-grade MVC tooling for FastAPI** — Beautiful interactive CLI for project scaffolding, entity generation, Alembic migrations, and the reference framework layout that ties together the FastMVC ecosystem (SQLAlchemy, Redis, JWT, and optional integrations).

**Python:** 3.10+

**Package name on PyPI:** `pyfastmvc`  
**Version:** see `[project]` in [`pyproject.toml`](pyproject.toml).

## Capabilities

- **Interactive CLI** — Beautiful terminal UI with Rich library for project generation
- **Auto venv setup** — Creates virtual environment, installs dependencies, updates `.gitignore`
- **VS Code integration** — Pre-configured debug profiles, tasks, and recommended extensions
- **Makefile** — Common development commands (dev, test, lint, migrate, docker)
- **Entity generation** — Scaffold controllers, services, repositories, and DTOs
- **Alembic migrations** — Database migration management
- **App template** — FastAPI app structure, configuration, middleware, and services expected by extension packages (`fast_*`)
- **Batteries** — FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, Redis, JWT, bcrypt, etc. (full list in `pyproject.toml` `dependencies`)

## Install

```bash
pip install pyfastmvc

# For best interactive experience
pip install pyfastmvc[interactive]
```

Editable from this directory (when developing the framework):

```bash
pip install -e .
```

## CLI Usage

### Interactive Project Generation

```bash
# Run the wizard
fastmvc generate

# Or with options
fastmvc generate --name my_api --author "John Doe"

# Quick start with defaults
fastmvc quickstart --name my_api
```

### Generated Project Features

Every generated project includes:

- **Virtual environment** — Auto-created at `.venv/` (configurable)
- **VS Code settings** — Debug configs, tasks, recommended extensions
- **Makefile** — `make dev`, `make test`, `make lint`, `make migrate`
- **Example API** — Working Item CRUD at `/items`
- **Test structure** — Unit and integration test setup

### Development Commands

```bash
cd my_api

# Using Makefile
make dev              # Start development server
make test             # Run tests
make lint             # Run linter
make format           # Format code
make migrate msg=""   # Create migration
make upgrade          # Apply migrations
make docker-up        # Start with Docker

# Using VS Code
# Press F5 to debug or Cmd/Ctrl+Shift+P → "Tasks: Run Task"
```

## Links

- **Repository:** [github.com/shregar1/fastMVC](https://github.com/shregar1/fastMVC) (see `[project.urls]` in `pyproject.toml`).
- **Docs:** [fastapi-mvc.dev](https://fastapi-mvc.dev/docs) (when published).

## Extension packages

The **`fast_*`** libraries in the monorepo are optional add-ons (DB, queues, LLM, storage, …). See the [parent README](../README.md) for the full package table and [`install_packages.sh`](../install_packages.sh) to install them in editable mode.

## Tooling

See [CONTRIBUTING.md](CONTRIBUTING.md), [Makefile](Makefile), and [PUBLISHING.md](PUBLISHING.md).

---

## Documentation

| Document | Purpose |
|----------|---------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Dev setup, tests, monorepo sync |
| [PUBLISHING.md](PUBLISHING.md) | PyPI and releases |
| [SECURITY.md](SECURITY.md) | Reporting vulnerabilities |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

**Monorepo:** [../README.md](../README.md) · **Coverage:** [../docs/COVERAGE.md](../docs/COVERAGE.md)
