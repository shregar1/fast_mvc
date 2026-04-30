# 🛠️ FastCLI

**The Vertical Slice Orchestrator & Scaffolding Engine.**

FastCLI is the primary developer interface for FastX. It transforms the framework's architectural philosophy into an automated developer experience.

---

## 🏗️ Core Scaffolding Features

FastCLI generates **complete vertical slices** in accordance with our per-version, per-operation folder structure.

| Command | Role | Impact |
|---------|------|--------|
| `generate` | **Project Wizard** | Creates a production-ready FastAPI project. |
| `add resource` | **Operation Slice** | Generates Controller, Service, DTO, Repository, Dependency. |
| `add auth` | **Security Stack** | Scaffolds logic for JWT, Login, Register, and MFA readiness. |
| `add middleware` | **ASGI Utilities** | Fast templates for rate limits, logging, and CORS. |
| `add test` | **Async Pytest** | Automatic test boilerplate with mock support. |
| `add task` | **Background Jobs** | Logic for asynchronous worker task orchestration. |
| `dockerize` | **Infrastructure** | Multi-stage Docker & healthchecked Compose config. |

---

## 🎯 Architectural Philosophy: Vertical Slices

FastCLI enforces **isolation at the operation level**. Instead of monolithic controllers, it scaffolds:

```text
v1/
  user/
    create.py    # Isolated Controller
    fetch.py     # Isolated Controller
```

This reduces merge conflicts, simplifies testing, and makes versioning (`v1` to `v2`) as simple as creating a new folder.

---

## 🛠️ Installation

FastCLI is available as a standalone CLI package:

```bash
pip install -e ./fastx_cli
```

Once installed, use it from anywhere:

```bash
fastx --help
```

---

## 🛰️ Documentation Generation

FastCLI includes an auto-doc engine:

```bash
fastx docs generate
```

It crawls your `apis/` and `dtos/` directories to build a complete **MkDocs API Reference site** using `mkdocstrings`.
