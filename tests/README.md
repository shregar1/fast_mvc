# Tests

## What this module does

The **`tests`** package contains **automated tests** for the FastMVC application: pytest modules, shared fixtures, and integration tests that exercise HTTP, database, and external boundaries. The goal is to **verify behavior** of controllers, services, repositories, and middleware without manual runs.

CI (e.g. GitHub Actions) typically runs **`pytest`** with options from **`pytest.ini`** and coverage thresholds from **`pyproject.toml`**.

## Layout (mirrors the app)

Place test modules under the same relative path as the code they exercise (e.g. factory tests under `tests/factories/apis/v1/example/`, Item API tests under `tests/example/` or `tests/controllers/apis/v1/item/`). Empty packages use `__init__.py` as placeholders until tests are added.

```text
tests/
├── conftest.py                    # Shared fixtures, markers, hooks
├── abstractions/                  # → abstractions/
├── apis/                          # → apis/
│   └── v1/
├── config/                        # → config/
├── constants/                     # → constants/
├── controllers/                   # → controllers/
├── core/                          # → core/
├── dependencies/                  # → dependencies/
├── dtos/                          # → dtos/
├── example/                       # → example/
│   └── test_example_item.py   # Item API (fixtures in tests/conftest.py)
├── factories/                     # → factories/
│   └── apis/
│       └── v1/
│           └── example/
│               └── test_factories_example.py
├── middlewares/                   # → middlewares/
├── repositories/                  # → repositories/
└── services/                      # → services/
```

Top-level **`factories/`** (not under `tests/`) provides **DTO-aligned builders**; see `factories/README.md` and `tests/factories/apis/v1/example/test_factories_example.py`. The **`fetch_example_request_payload`** fixture in `conftest.py` is wired from `ExampleFetchRequestFactory`.

## Types of tests

| Type | Purpose |
|------|---------|
| **Unit** | Services, repositories in isolation (mocks/fakes) |
| **API / integration** | `TestClient` / HTTP against real or test app |
| **Contract** | DTO validation, response shapes (optional) |

## How it fits in the stack

Tests mirror the **production** structure: they import from `services`, `repositories`, `models`, etc., and may use **`tests/factories/apis/v1/item`**, **`tests/conftest.py`**, or **`core/testing`** factories and mocks.

## Related files

- **`pytest.ini`** — markers, defaults  
- **`pytest.ini` / `pyproject.toml`** — coverage and plugins  
- **`tests/factories/apis/v1/item/`** (`create.py`, `create_batch.py`) / **`tests/conftest.py`** — Item factory and fixtures for Item API tests  

## Practices

1. **Mark** slow or integration tests (`pytest.mark.integration`) for selective runs.  
2. **Use** environment variables or test DB URLs for isolation.  
3. **Avoid** flaky tests; use deterministic seeds and clock mocks where needed.  
4. **Run** `pytest` before opening PRs; fix failures locally first.
