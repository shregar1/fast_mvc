# 🌌 The FastX Ecosystem

FastX is more than just a framework; it's a modular ecosystem of specialized packages designed to handle every layer of a production-grade application.

Each package is decoupled and can be used independently, but they are designed to work together seamlessly within the FastX architecture.

---

## 📦 Core Packages

| Package | Role | Key Feature |
|---------|------|-------------|
| [**FastX CLI**](fastx-cli.md) | **Orchestration** | Vertical slice scaffolding & dev-ops automation. |
| [**FastX Database**](fastx-database.md) | **Persistence** | Production-ready SQLAlchemy models, Mixins, and Repositories. |
| [**FastX Middleware**](fastx-middleware.md) | **Cross-Cutting** | 90+ ASGI middlewares for security, performance, and observability. |
| [**FastX Dashboards**](fastx-dashboards.md) | **Operations** | HTML dashboards for health, logs, and embedded analytics. |
| [**FastX Channels**](fastx-channels.md) | **Real-Time** | WebSocket channel abstraction with pub/sub rooms and presence tracking. |
| [**FastX Platform**](fastx-platform.md) | **Infrastructure** | Unified distribution for 60+ services (Messaging, Search, LLM, etc.). |

---

## 🛠️ Philosophy: Modular & Decoupled

The FastX ecosystem follows a **"Flat but Deep"** philosophy:
- **Flat Imports:** All packages under `fastx_platform` use top-level imports (e.g., `from notifications import ...`) to keep your code clean.
- **Deep Functionality:** Each module handles the complexities of its domain (e.g., `fastx_middleware` handles HSTS, CSP, and Rate Limiting automatically).
- **Vendor Friendly:** You can choose to vendor specific parts of the ecosystem into your project or install them as standalone wheels.

---

## 🚀 Getting Started with the Ecosystem

If you are using the FastX CLI, most of these packages are already available in your environment. You can explore them in your `src/` or `fastx_<package>/` directories.

To install a specific part of the ecosystem in any Python project:
```bash
pip install fastx-platform      # Get the whole platform
pip install fastx-database      # Persistence only
pip install fastx-middleware    # HTTP utilities only
```
