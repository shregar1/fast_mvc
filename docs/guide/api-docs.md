# API Documentation

FastMVC provides branded **Swagger UI** and **ReDoc** plus the machine-readable **OpenAPI JSON** schema. In production you should treat these as **developer-only** surfaces: they expose your full API surface area.

## Swagger UI

FastMVC includes a custom Swagger UI with FastMVC branding:

### Dark Theme

The Swagger UI uses a custom dark theme with the following color scheme:

- **Primary Color**: Cyan (`#0ea5e9`)
- **Accent Color**: Fuchsia (`#d946ef`)
- **Background**: Dark slate (`#0f0f1a`)

### Features

- FastMVC-branded dark theme
- Code syntax highlighting
- Copy buttons for code samples
- Example requests in multiple languages
- Interactive "Try It Out" feature

### Accessing Swagger UI

Once your server is running, visit:

```text
http://localhost:8000/docs
```

Subpaths under `/docs` (for example OAuth redirects used by Swagger UI) are served from the same app and follow the same access rules as `/docs` itself.

## ReDoc

FastMVC also provides a ReDoc interface for API documentation:

```text
http://localhost:8000/redoc
```

ReDoc offers:

- Clean, three-pane layout
- Search functionality
- Grouped endpoints
- Schema exploration

## OpenAPI Schema

The raw OpenAPI document is served at a configurable URL (default below). Use it to generate clients, import into Postman, or run contract tests.

```text
http://localhost:8000/openapi.json
```

The path is controlled by **`OPENAPI_URL`** and must stay aligned with the FastAPI app and with the documentation auth middleware (see below).

---

## Securing Swagger, ReDoc, and OpenAPI (recommended for production)

End users should not need interactive API explorers on a public deployment. FastMVC can require **HTTP Basic authentication** for all documentation and schema routes when you set **both**:

| Variable | Purpose |
|----------|---------|
| `DOCS_USERNAME` | Basic auth user name (non-empty after trim) |
| `DOCS_PASSWORD` | Basic auth password (non-empty after trim) |

If **either** variable is missing or empty, documentation routes stay **unauthenticated** (typical for local development).

### What is protected

When `DOCS_USERNAME` and `DOCS_PASSWORD` are set, the following require a valid `Authorization: Basic …` header:

- **`/docs`** and **any path under `/docs/`** (for example `/docs/oauth2-redirect`), but not unrelated paths like `/documentation`.
- **`/redoc`** and **any path under `/redoc/`**.
- The **OpenAPI JSON** URL: primary path from **`OPENAPI_URL`** (default `/openapi.json`), plus any extra paths listed in **`DOCS_EXTRA_PROTECTED_PATHS`** (comma-separated).

`OPTIONS` requests to these routes are **not** challenged so **CORS preflight** can succeed before the browser sends credentialed `GET` requests.

### Additional environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAPI_URL` | `/openapi.json` | Must match `FastAPI(openapi_url=…)` in `app.py`. Normalized with a leading `/`. |
| `DOCS_EXTRA_PROTECTED_PATHS` | *(empty)* | Comma-separated list of extra paths that must use the same Basic auth (for example a legacy schema URL). |

See **`.env.example`** in the repo for commented examples.

### Nginx

If you terminate TLS or reverse-proxy in front of the app (for example `_maint/nginx/nginx.conf`), proxy **prefix** locations for `/docs` and `/redoc` so all subpaths reach the app. Add an exact (or prefix) location for your **`OPENAPI_URL`** path; if you change `OPENAPI_URL` away from `/openapi.json`, add a matching `location` in nginx—the application does not rewrite nginx for you.

### Implementation

- Middleware: `middlewares/docs_auth.py` (`DocsBasicAuthMiddleware`)
- Helpers: `DocsAuthConfig.normalized_openapi_url()`, `DocsAuthConfig.resolve_openapi_url_paths()`, `DocsAuthConfig.docs_logging_exclude_paths()`
- Request logging excludes the same doc/schema paths so high-frequency UI traffic does not flood access logs.

### Calling the schema from scripts

```bash
curl -u "$DOCS_USERNAME:$DOCS_PASSWORD" "https://api.example.com/openapi.json"
```

---

## Customization

### Modifying the Theme

Edit `static/swagger.html` to customize:

```html
<style>
  :root {
    --fastmvc-primary: #your-primary-color;
    --fastmvc-accent: #your-accent-color;
  }
</style>
```

### Adding Examples

Add example responses to your endpoints:

```python
from fastapi import FastAPI
from pydantic import IModel

class Item(IModel):
    name: str
    price: float

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    """
    Get an item by ID.

    Example response:
    ```json
    {
        "name": "Sample Item",
        "price": 29.99
    }
    ```
    """
    return Item(name="Sample Item", price=29.99)
```

---

## MkDocs Documentation

For comprehensive documentation, FastMVC includes MkDocs with Material theme:

### Commands

```bash
# Install documentation dependencies
make docs-install

# Serve documentation locally
make docs-serve

# Build static documentation
make docs-build

# Deploy to GitHub Pages
make docs-deploy
```

### Features

- Dark mode by default
- Automatic API reference generation
- Search functionality
- Code copy buttons
- Responsive design
