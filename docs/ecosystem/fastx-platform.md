# 💎 FastPlatform

**Unified distribution for the entire FastX Ecosystem.**

FastPlatform is a single installable package that bundles 60+ standalone services. It follows a **package taxonomy** that organizes imports while keeping them flat and easy to use.

---

## 🏗️ Package Taxonomy

FastPlatform is organized into functional sections defined in `fastx_platform.taxonomy`:

| Section | Role | Key Packages |
|---------|------|--------------|
| **`core`** | **Foundational** | `configuration`, `dtos`, `errors`, `utils`. |
| **`security`** | **Identity & Access** | `identity`, `secrets`, `security`, `rbac`, `sessions`, `api_keys`. |
| **`persistence`** | **Data Access** | `db`, `datastores`, `query_builder`, `sharding`, `event_sourcing`. |
| **`messaging`** | **Async Communication** | `kafka`, `queues`, `jobs`, `notifications`, `message_bus`. |
| **`realtime`** | **Streams** | `channels`, `streams`, `webrtc`, `sse`, `collaboration`. |
| **`operations`** | **Observability** | `observability`, `otel`, `resilience`, `tenancy`, `alerting`, `profiler`. |
| **`integrations`** | **Third-Party** | `llm`, `payments`, `media`, `search`, `vectors`. |
| **`devtools`** | **Developer Experience** | `api_fuzzer`, `http_cassette`, `iac`, `db_studio`, `api_explorer`. |

---

## 🔐 Authentication & Identity

| Module | Description |
|--------|-------------|
| `webauthn` | FIDO2/WebAuthn passkey registration and authentication. |
| `magic_link` | Passwordless email-based login flows. |
| `oauth2_server` | Full OAuth 2.0 authorization server with PKCE support. |
| `totp` | Time-based one-time password (MFA) generation and verification. |
| `social_login` | Pre-built providers for Google, GitHub, Apple, and more. |
| `rbac` | Role-based access control with hierarchical permissions. |
| `sessions` | Secure server-side session management with pluggable stores. |
| `api_keys` | API key issuance, rotation, and scoped access control. |

---

## 💾 Data & Persistence

| Module | Description |
|--------|-------------|
| `query_builder` | Fluent, composable query construction for SQLAlchemy and raw SQL. |
| `cdc` | Change Data Capture streams for real-time data synchronization. |
| `anonymization` | PII masking and data anonymization utilities for GDPR compliance. |
| `sharding` | Horizontal database sharding with automatic routing. |
| `event_sourcing` | Event store, projections, and aggregate root patterns. |

---

## 📬 Messaging & Communication

| Module | Description |
|--------|-------------|
| `message_bus` | In-process and distributed command/event bus. |
| `push_notifications` | Unified push via APNs, FCM, and Web Push. |
| `email` | Transactional email with Postmark, SendGrid, and SES backends. |
| `sms` | SMS delivery through Twilio, Vonage, and SNS. |
| `sse` | Server-Sent Events for one-way real-time push to clients. |

---

## 🌐 API Infrastructure

| Module | Description |
|--------|-------------|
| `api_versioning` | URL, header, and query-param based API versioning strategies. |
| `api_analytics` | Request-level analytics with latency percentiles and error rates. |
| `problem_details` | RFC 9457 Problem Details for HTTP API error responses. |
| `request_coalescing` | Deduplicate identical in-flight requests to reduce backend load. |
| `grpc_gateway` | Expose gRPC services as REST endpoints with automatic transcoding. |
| `graphql_subscriptions` | Real-time GraphQL subscriptions over WebSocket transport. |

---

## 🛡️ DevOps & Reliability

| Module | Description |
|--------|-------------|
| `chaos` | Chaos engineering primitives — fault injection, latency simulation. |
| `canary` | Canary deployment traffic splitting and metric comparison. |
| `performance_budgets` | Enforce response-time and payload-size budgets per endpoint. |
| `contract_testing` | Consumer-driven contract tests for service boundaries. |
| `circuit_breaker` | Circuit breaker pattern with configurable thresholds and fallbacks. |
| `alerting` | Rule-based alerting with Slack, PagerDuty, and webhook delivery. |

---

## 📄 Content & Media

| Module | Description |
|--------|-------------|
| `cms` | Headless CMS with structured content types and draft/publish workflow. |
| `image_processing` | On-the-fly image resize, crop, and format conversion. |
| `pdf` | PDF generation from HTML templates with Weasyprint or Puppeteer. |
| `storage` | Unified object storage interface for S3, GCS, and Azure Blob. |

---

## 🧰 Developer Tools

| Module | Description |
|--------|-------------|
| `api_fuzzer` | Automated API fuzz testing with schema-aware payload generation. |
| `http_cassette` | Record and replay HTTP interactions for deterministic tests. |
| `iac` | Infrastructure-as-Code templates for Terraform and Pulumi. |
| `profiler` | Request-level profiling with flame graph visualization. |
| `db_studio` | Browser-based database explorer and query runner. |
| `api_explorer` | Interactive API playground with authentication presets. |

---

## 🔍 Search & AI

| Module | Description |
|--------|-------------|
| `search` | Full-text search with Meilisearch, Elasticsearch, and Typesense backends. |
| `vectors` | Vector embedding storage and similarity search for RAG pipelines. |
| `llm` | Unified LLM interface for OpenAI, Anthropic, and local models. |

---

## 🏢 Infrastructure

| Module | Description |
|--------|-------------|
| `rate_limiter` | Token-bucket and sliding-window rate limiting with Redis backend. |
| `i18n` | Internationalization with message catalogs and locale negotiation. |
| `multitenancy` | Tenant isolation via schema, database, or row-level strategies. |
| `scheduler` | Cron-like task scheduling with distributed locking. |
| `jobs` | Background job processing with retries and dead-letter queues. |
| `secrets` | Secrets management with Vault, AWS Secrets Manager, and .env fallback. |
| `configuration` | Layered configuration from env, files, and remote providers. |
| `request_replay` | Capture and replay production requests for debugging. |
| `collaboration` | Real-time collaborative editing with CRDT-based conflict resolution. |
| `feature_flags` | Feature flag evaluation with percentage rollouts and targeting rules. |
| `webhook_receiver` | Inbound webhook ingestion with signature verification and retries. |
| `data_export` | Bulk data export in CSV, Parquet, and JSON Lines formats. |

---

## ⚡ Multi-Backend Capabilities

FastPlatform is designed for high-scale, multi-backend environments:
- **Notifications:** Single interface for Email (Postmark, SendGrid), SMS (Twilio), and Push.
- **DataStores:** Generic `IDataStore` adapters for Redis, MongoDB, and Elasticsearch.
- **Storage:** Unified `S3`, `GCS`, and `Azure` object storage interface.
- **Search:** Swap between Meilisearch, Elasticsearch, and Typesense with one config change.
- **LLM:** Provider-agnostic interface across OpenAI, Anthropic, and local models.
- **Resilience:** Circuit breakers and retries are first-class citizens.

---

## 🎨 Flat Imports (Developer Velocity)

Despite being a massive distribution, FastPlatform keeps your imports simple:
```python
from notifications import send_email
from db import DBDependency
from errors import BadInputError
from versioning import VersionedAPIRouter
from search import SearchIndex
from llm import complete
```

---

## 🚀 Optional Feature Extras

To keep your lean Docker images small, you can install only what you need:
- **`async`**: Async-native client extras.
- **`otel`**: OpenTelemetry tracing & metrics support.
- **`s3`**: AWS S3 object storage dependencies.
- **`openai`**: LLM provider SDKs.
- **`redis`**: Redis-backed rate limiting, caching, and pub/sub.
- **`grpc`**: gRPC gateway and protobuf support.
- **`vectors`**: Vector database client libraries.

---

## 🛠️ Installation

FastPlatform is the recommended way to use the ecosystem in your API:
```bash
pip install fastx-platform
```

Run with all the bells and whistles:
```bash
pip install fastx-platform[async,otel,s3,openai,meilisearch,redis,grpc,vectors]
```
