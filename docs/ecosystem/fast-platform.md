# 💎 FastPlatform

**Unified distribution for the entire FastX Ecosystem.**

FastPlatform is a single installable package that bundles 30+ standalone services. It follows a **package taxonomy** that organizes imports while keeping them flat and easy to use.

---

## 🏗️ Package Taxonomy

FastPlatform is organized into functional sections defined in `fastx_platform.taxonomy`:

| Section | Role | Key Packages |
|---------|------|--------------|
| **`core`** | **Foundational** | `configuration`, `dtos`, `errors`, `utils`. |
| **`security`** | **Identity** | `identity`, `secrets`, `security`. |
| **`persistence`** | **Data Access** | `db`, `datastores`. |
| **`messaging`** | **Async Communication** | `kafka`, `queues`, `jobs`, `notifications`. |
| **`realtime`** | **Streams** | `channels`, `streams`, `webrtc`. |
| **`operations`** | **Observability** | `observability`, `otel`, `resilience`, `tenancy`. |
| **`integrations`** | **Third-Party** | `llm`, `payments`, `media`, `search`. |

---

## ⚡ Multi-Backend Capabilities

FastPlatform is designed for high-scale, multi-backend environments:
- **Notifications:** Single interface for Email (Postmark, SendGrid), SMS (Twilio), and Push.
- **DataStores:** Generic `IDataStore` adapters for Redis, MongoDB, and Elasticsearch.
- **Storage:** Unified `S3`, `GCS`, and `Azure` object storage interface.
- **Resilience:** Circuit breakers and retries are first-class citizens.

---

## 🎨 Flat Imports (Developer Velocity)

Despite being a massive distribution, FastPlatform keeps your imports simple:
```python
from notifications import send_email
from db import DBDependency
from errors import BadInputError
from versioning import VersionedAPIRouter
```

---

## 🚀 Optional Feature Extras

To keep your lean Docker images small, you can install only what you need:
- **`async`**: Async-native client extras.
- **`otel`**: OpenTelemetry tracing & metrics support.
- **`s3`**: AWS S3 object storage dependencies.
- **`openai`**: LLM provider SDKs.

---

## 🛠️ Installation

FastPlatform is the recommended way to use the ecosystem in your API:
```bash
pip install fast-platform
```

Run with all the bells and whistles:
```bash
pip install fast-platform[async,otel,s3,openai,meilisearch]
```
