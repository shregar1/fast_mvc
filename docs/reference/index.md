# Reference

Complete API reference for FastMVC components.

## Abstractions

### BaseEntity

Base class for all domain entities.

```python
from abstractions.entity import BaseEntity

class Item(BaseEntity):
    id: int
    name: str
    description: str | None = None
```

### BaseRepository

Base repository pattern implementation.

```python
from abstractions.repository import BaseRepository

class ItemRepository(BaseRepository[Item]):
    async def get_by_name(self, name: str) -> Item | None:
        # Custom query
        pass
```

### BaseService

Base service layer.

```python
from abstractions.service import BaseService

class ItemService(BaseService[Item]):
    async def create_with_defaults(self, data: dict) -> Item:
        # Custom business logic
        pass
```

### BaseController

Base controller for HTTP handling.

```python
from abstractions.controller import BaseController

controller = BaseController(ItemService, Item)
```

## DTOs

### BaseDTO

Base data transfer object.

```python
from dtos.base import BaseDTO

class CreateItemRequest(BaseDTO):
    name: str
    description: str | None = None
```

## Core Utilities

### Database

```python
from core.database import get_db, Database

db = Database("sqlite:///./app.db")
```

### Cache

```python
from core.cache import Cache

cache = Cache("redis://localhost:6379")
await cache.set("key", "value", ttl=3600)
```

### Logging

```python
from core.logging import get_logger

logger = get_logger("my_module")
logger.info("Message", extra={"key": "value"})
```

### Pagination

```python
from core.pagination import PaginatedResponse, PaginationParams

params = PaginationParams(skip=0, limit=10)
response = PaginatedResponse(items=[], total=0)
```

## Middlewares

### Request Logging

```python
from middlewares.request_logging import RequestLoggingMiddleware

app.add_middleware(RequestLoggingMiddleware)
```

### Error Handling

```python
from middlewares.error_handling import ErrorHandlingMiddleware

app.add_middleware(ErrorHandlingMiddleware)
```

### Rate Limiting

```python
from middlewares.rate_limiting import RateLimitMiddleware

app.add_middleware(
    RateLimitMiddleware,
    requests_per_minute=100
)
```

## Configuration

### Settings

```python
from config.settings import Settings

settings = Settings()
print(settings.app_name)
```

### Validator

```python
from config.validator import validate_config_or_exit

validate_config_or_exit()
```
