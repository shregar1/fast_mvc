# Project Structure

Understanding the FastMVC project layout and organization.

## Directory Overview

```
my-project/
├── app.py                      # Application entry point
├── pyproject.toml             # Project metadata and dependencies
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
├── requirements-docs.txt      # Documentation dependencies
├── Makefile                   # Development commands
├── .env                       # Environment variables (git-ignored)
├── .env.example               # Example environment file
├── .pre-commit-config.yaml    # Pre-commit hooks
├── docker-compose.yml         # Docker services
├── Dockerfile                 # Container definition
│
├── abstractions/              # Base classes and interfaces
│   ├── controller.py         # Base controller with CRUD
│   ├── repository.py         # Base repository pattern
│   ├── service.py            # Base service layer
│   └── entity.py             # Base entity/model
│
├── config/                    # Configuration
│   ├── settings.py           # Pydantic settings
│   └── validator.py          # Environment validation
│
├── constants/                 # Application constants
│   ├── http.py               # HTTP status codes
│   ├── messages.py           # Response messages
│   └── default.py            # Default values
│
├── core/                      # Core utilities
│   ├── database.py           # Database connection
│   ├── cache.py              # Caching utilities
│   ├── logging.py            # Logging configuration
│   ├── exceptions.py         # Custom exceptions
│   ├── pagination.py         # Pagination helpers
│   ├── responses.py          # Response utilities
│   ├── docs.py               # API documentation setup
│   └── testing/              # Testing utilities
│       └── fixtures.py
│
├── dependencies/              # FastAPI dependencies
│   ├── database.py           # DB session injection
│   └── auth.py               # Authentication deps
│
├── docs/                      # Documentation
│   ├── index.md
│   ├── guide/
│   ├── api/
│   └── stylesheets/
│
├── dtos/                      # Data Transfer Objects
│   ├── base.py               # Base DTO classes
│   ├── request.py            # Request DTOs
│   └── response.py           # Response DTOs
│
├── example/                   # Example API implementation
│   ├── entity.py             # Item entity
│   ├── repository.py         # Item repository
│   ├── service.py            # Item service
│   ├── controller.py         # Item controller
│   └── __init__.py
│
├── middlewares/               # FastAPI middleware
│   ├── request_logging.py    # Request logging
│   ├── error_handling.py     # Error handling
│   ├── rate_limiting.py      # Rate limiting
│   ├── cors.py               # CORS setup
│   └── timing.py             # Request timing
│
├── static/                    # Static files
│   └── swagger.html          # Custom Swagger UI
│
├── scripts/                   # Utility scripts
│   └── setup.sh
│
├── tests/                     # Test suite
│   ├── conftest.py           # Pytest configuration
│   ├── test_example.py       # Example tests
│   └── utils/
│
└── .vscode/                   # VS Code settings
    ├── settings.json
    ├── launch.json
    ├── tasks.json
    └── extensions.json
```

## Layer Explanation

### 1. Abstractions Layer

Base classes that define the contract for each layer:

- **Entity**: Domain models
- **Repository**: Data access interface
- **Service**: Business logic interface
- **Controller**: HTTP handling interface

### 2. Core Layer

Shared utilities and infrastructure:

- **Database**: Connection management, sessions
- **Cache**: Redis integration
- **Logging**: Structured logging setup
- **Exceptions**: Custom exception classes
- **Responses**: Standard response formats

### 3. Feature Layer (Example)

Each feature follows the MVC pattern:

```
example/
├── entity.py      # Data model
├── repository.py  # Data access
├── service.py     # Business logic
└── controller.py  # HTTP endpoints
```

## Design Principles

### Separation of Concerns

Each layer has a single responsibility:
- **Controller**: Handles HTTP requests/responses
- **Service**: Contains business logic
- **Repository**: Handles data persistence
- **Entity**: Defines data structure

### Dependency Inversion

Higher-level modules depend on abstractions:

```python
# Service depends on Repository abstraction
class ItemService(BaseService):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

# Repository depends on Entity
class ItemRepository(BaseRepository):
    def __init__(self, entity_class: Type[BaseEntity]):
        self.entity_class = entity_class
```

### Dependency Injection

FastAPI's dependency system wires everything together:

```python
@router.get("/items")
async def list_items(
    service: ItemService = Depends(get_item_service)
):
    return await service.list()
```

## Adding New Features

To add a new feature (e.g., `users`):

1. **Create the feature directory**:
```bash
mkdir users
touch users/__init__.py
```

2. **Define the entity**:
```python
# users/entity.py
from abstractions.entity import BaseEntity

class User(BaseEntity):
    id: int
    email: str
    name: str
```

3. **Create the repository**:
```python
# users/repository.py
from abstractions.repository import BaseRepository
from users.entity import User

class UserRepository(BaseRepository[User]):
    pass
```

4. **Create the service**:
```python
# users/service.py
from abstractions.service import BaseService
from users.repository import UserRepository

class UserService(BaseService[User]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)
```

5. **Create the controller**:
```python
# users/controller.py
from fastapi import APIRouter
from abstractions.controller import BaseController
from users.service import UserService

router = APIRouter(prefix="/users")
controller = BaseController(UserService, User)

@router.get("")
async def list_users():
    return await controller.list()
```

6. **Register in app.py**:
```python
from users.controller import router as users_router
app.include_router(users_router, tags=["users"])
```

## Best Practices

1. **Keep controllers thin**: Only HTTP-related logic
2. **Keep services pure**: No HTTP or DB dependencies
3. **Use DTOs**: Separate request/response models from entities
4. **Handle errors**: Use custom exceptions and middleware
5. **Write tests**: Test each layer independently
6. **Document APIs**: Use docstrings and type hints
