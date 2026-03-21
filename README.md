# pyfastmvc

**Production-grade MVC tooling for FastAPI** — CLI entrypoint, project scaffolding, entity generation, Alembic migrations, and the reference framework layout that ties together the FastMVC ecosystem (SQLAlchemy, Redis, JWT, and optional integrations).

**Python:** 3.10+

**Package name on PyPI:** `pyfastmvc`  
**Version:** see `[project]` in [`pyproject.toml`](pyproject.toml).

## Capabilities

- **CLI** — the `fastmvc` command (`fastmvc_cli.cli:main`) generates projects, resources, and migrations (see `[project.scripts]` in `pyproject.toml`).
- **App template** — FastAPI app structure, configuration, middleware, and services expected by extension packages (`fastmvc_*`).
- **Batteries** — FastAPI, SQLAlchemy 2, Alembic, Pydantic v2, Redis, JWT, bcrypt, etc. (full list in `pyproject.toml` `dependencies`).

## Install

```bash
pip install pyfastmvc
```

Editable from this directory (when developing the framework):

```bash
pip install -e .
```

## Links

- **Repository:** [github.com/shregar1/fastMVC](https://github.com/shregar1/fastMVC) (see `[project.urls]` in `pyproject.toml`).
- **Docs:** [fastapi-mvc.dev](https://fastapi-mvc.dev/docs) (when published).

## Extension packages

The **`fastmvc_*`** libraries in the monorepo are optional add-ons (DB, queues, LLM, storage, …). See the [parent README](../README.md) for the full package table and [`install_packages.sh`](../install_packages.sh) to install them in editable mode.

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
