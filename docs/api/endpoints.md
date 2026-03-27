# API Endpoints

Complete reference for all API endpoints.

## Health Endpoints

### GET /health

Comprehensive health check with dependency status.

**Description:** Performs health checks on application, database, and Redis cache.

**Response (200 OK - Healthy):**
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "version": "1.5.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "uptime_seconds": 3600
}
```

**Response (503 Service Unavailable - Unhealthy):**
```json
{
  "status": "unhealthy",
  "database": "disconnected: connection refused",
  "redis": "connected",
  "version": "1.5.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### GET /health/live

Kubernetes liveness probe.

**Description:** Lightweight check that indicates the application process is running. Used by Kubernetes to determine if the container should be restarted.

**Response (200 OK):**
```json
{"status": "alive"}
```

### GET /health/ready

Kubernetes readiness probe.

**Description:** Checks if the application is ready to receive traffic. Verifies database and Redis connectivity.

**Response (200 OK - Ready):**
```json
{
  "status": "ready",
  "timestamp": "2024-01-01T00:00:00Z",
  "checks": {
    "database": "connected",
    "redis": "connected"
  }
}
```

**Response (503 Service Unavailable - Not Ready):**
```json
{
  "status": "not_ready",
  "timestamp": "2024-01-01T00:00:00Z",
  "checks": {
    "database": "disconnected: connection timeout",
    "redis": "connected"
  }
}
```

---

## Items API

### GET /items

List all items with optional filtering and pagination.

### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

## Items

### GET /items

List all items with optional filtering and pagination.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Number of items to skip |
| limit | int | Maximum items to return |
| completed | bool | Filter by completion status |
| search | string | Search in name/description |

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Buy milk",
      "description": "Get from store",
      "completed": false,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### GET /items/{id}

Get a specific item by ID.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | int | Item ID |

**Response:**
```json
{
  "id": 1,
  "name": "Buy milk",
  "description": "Get from store",
  "completed": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### POST /items

Create a new item.

**Request Body:**
```json
{
  "name": "Buy milk",
  "description": "Get from store",
  "completed": false
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Buy milk",
  "description": "Get from store",
  "completed": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### PUT /items/{id}

Update an existing item.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | int | Item ID |

**Request Body:**
```json
{
  "name": "Buy organic milk",
  "description": "Get from organic store",
  "completed": true
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Buy organic milk",
  "description": "Get from organic store",
  "completed": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

### DELETE /items/{id}

Delete an item.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | int | Item ID |

**Response:**
```json
{
  "message": "Item deleted successfully"
}
```

### PATCH /items/{id}/toggle

Toggle the completion status of an item.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | int | Item ID |

**Response:**
```json
{
  "id": 1,
  "name": "Buy milk",
  "completed": true
}
```

### GET /items/stats

Get item statistics.

**Response:**
```json
{
  "total": 10,
  "completed": 5,
  "pending": 5
}
```

## Error Responses

### 404 Not Found

```json
{
  "detail": "Item not found"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Server Error

```json
{
  "detail": "Internal server error"
}
```
