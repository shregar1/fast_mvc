# fast-mvc

**Production-grade MVC tooling for FastAPI** — Beautiful interactive CLInterface for project scaffolding, entity generation, Alembic migrations, and the reference framework layout that ties together the FastMVC ecosystem (SQLAlchemy, Redis, JWT, and optional integrations).

**Python:** 3.10+

**Package name on PyPI:** `fast-mvc`  
**Version:** see `[project]` in [`pyproject.toml`](pyproject.toml).

## Capabilities

- **Interactive CLI** — Beautiful terminal UI with Rich library for project generation
- **Auto venv setup** — Creates virtual environment, installs dependencies, updates `.gitignore`
- **VS Code integration** — Pre-configured debug profiles, tasks, and recommended extensions
- **Makefile** — Common development commands (dev, test, lint, migrate, docker)
- **Entity generation** — Scaffold controllers, services, repositories, and DTOs
- **Alembic migrations** — DataI migration management via CLI
- **App template** — FastAPI app structure, configuration, middleware, and services expected by extension packages (`fast_*`)
- **Batteries** — FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, Redis, JWT, bcrypt, etc.

### New Features

- **DataI Migration CLI** — `fastmvc db migrate/upgrade/downgrade/reset`
- **Testing Framework** — ItemFactory, pytest fixtures, auth mocks
- **Docker Compose Stack** — One-command full setup (Postgres + Redis + FastAPI)
- **GitHub Actions CI/CD** — Auto-generated workflows for every project
- **Dark-themed API Docs** — FastMVC-branded Swagger UI with dark mode
- **Production Health Checks** — Kubernetes-ready endpoints

## Install

```bash
pip install fast-mvc

# For best interactive experience
pip install fast-mvc[interactive]
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

## Feature Details

### DataI Migration CLI

Manage database migrations directly from the CLI:

```bash
# Create migration from model changes
fastmvc db migrate -m "Add users table"

# Apply migrations
fastmvc db upgrade

# Rollback one migration
fastmvc db downgrade

# Reset database (development only)
fastmvc db reset --seed

# Check status
fastmvc db status
```

### Docker Compose Stack

One command starts the full stack:

```bash
# Start everything (Postgres, Redis, FastAPI + migrations)
make docker-up

# Start with development tools (PgAdmin, Redis Insight)
make docker-up-dev

# Access points:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - PgAdmin: http://localhost:5050
# - Redis Insight: http://localhost:5540
```

### Testing Framework

Generated projects include comprehensive testing utilities:

```python
from tests.factories.apis.v1.item import ItemFactory
# Shared fixtures: tests/conftest.py (Item API + shared pytest fixtures)

# Generate fake test data
item = ItemFactory.create(name="Test Item", completed=True)

# Use fixtures in tests
def test_create_item(item_client, create_item_payload, mock_auth):
    with mock_auth:
        response = item_client.post("/items", json=create_item_payload)
        assert response.status_code == 201
```

### GitHub Actions CI/CD

Auto-generated workflows include:

- **CI/CD workflow** — Test, lint, build Docker images
- **PR Checks** — Fast validation and test runs
- **Release workflow** — Build and push on version tags

### API Documentation

- Dark-themed Swagger UI at `/docs`
- FastMVC branding with cyan/fuchsia color scheme
- Kubernetes health endpoints at `/health`, `/health/live`, `/health/ready`

### Postman collection

The repo includes `postman_collection.json` (and optionally `postman_environment.json`). They are produced from the **same export path** as application startup (`app.on_startup` → `RouteExportEngine`), so the OpenAPI-derived requests, folder layout, and tests stay aligned with `core/route_export_engine.py`. Prefer **regenerating** over hand-editing structure.

**Regenerate** (same Python environment as `make dev`; run from this directory):

```bash
make postman-export
# or: python3 _maint/scripts/export_postman_collection.py
```

If startup validation blocks the import, ensure `.env` exists (see `.env.example`) or set `VALIDATE_CONFIG=false` for a one-off export.

**Environment variables** (also listed in the `app.py` module docstring; values match what the server uses on boot):

| Variable | Purpose |
|----------|---------|
| `POSTMAN_EXPORT_ENVIRONMENT` | Set to `1` or `true` to also write `postman_environment.json` (default is collection-only). |
| `POSTMAN_COLLECTION_NAME` | Override the collection/environment title (default: git repository folder name). |
| `POSTMAN_BASE_URL` | Override the `base_url` variable (default: `http://HOST:PORT` from env). |
| `POSTMAN_ENV_FILE` | Filename for the optional environment export (default: `postman_environment.json`). |
| `POSTMAN_NEGATIVE_TESTS` | Set to `0` or `false` to skip extra per-request `pm.sendRequest` “negative” scripts. |

On startup, the app logs the written paths and variable names, for example: `variables: base_url, reference_urn, reference_number, token, refresh_token`.

**Login responses (`data.tokens`)** — After a successful login that returns the standard envelope with JWTs under `data` (e.g. `data.tokens.accessToken`, `data.tokens.refreshToken`), the collection **test** script fills the `token` and `refresh_token` collection variables so `Authorization: Bearer {{token}}` works on later requests. Supports camelCase (`accessToken`) and snake_case (`access_token`) field names.

**After importing into Postman** (quick verification):

- Open the collection **Variables** tab and confirm `base_url` is the server you intend to hit (e.g. `http://localhost:8000`).
- Send one request and confirm `{{reference_urn}}` on `x-reference-urn` and JSON bodies behave as expected; run login first or set `token` manually if the route uses Bearer auth.
- **Collection Runner** executes tests, including negative cases that issue additional HTTP calls to `{{base_url}}`. Use a dev or staging URL before running the full collection against a shared or production API.

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
