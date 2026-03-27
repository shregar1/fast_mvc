# Authentication

FastMVC supports Bearer token authentication using JWT.

## Login

Obtain an access token:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "user@example.com",
    "password": "secretpassword"
  }'
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

## Using the Token

Include the token in the Authorization header:

```bash
curl http://localhost:8000/items \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Token Refresh

Refresh an expiring token:

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: Bearer YOUR_REFRESH_TOKEN"
```

## Logout

Invalidate the current token:

```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Protected Endpoints

The following endpoints require authentication:

- `POST /items`
- `PUT /items/{id}`
- `DELETE /items/{id}`

Public endpoints:

- `GET /health`
- `GET /docs`
- `GET /redoc`
- `GET /openapi.json`
