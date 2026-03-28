"""Tests for FastMVC authentication middleware wiring."""

from __future__ import annotations

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from http import HTTPStatus

from middlewares.authentication import AuthenticationMiddleware


def test_auth_middleware_wiring():
    """Verify AuthenticationMiddleware is correctly configured and injectable."""
    app = FastAPI()
    
    # If AuthenticationMiddleware is configured (partial or class), add it
    if AuthenticationMiddleware:
        app.add_middleware(AuthenticationMiddleware)
    
    @app.get("/test-protected")
    async def protected_route():
        return {"message": "success"}

    client = TestClient(app)
    
    # If it's the real JWT middleware (not NoOp), it should block by default
    # If it's NoOp (development fallback), it will pass.
    response = client.get("/test-protected")
    
    # We just want to ensure it doesn't crash during initialization and dispatch
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.UNAUTHORIZED)

@pytest.mark.asyncio
async def test_auth_noop_fallback():
    """Ensure the fallback middleware works when dependencies are missing."""
    from middlewares.authentication import NoOpAuthMiddleware
    
    app = FastAPI()
    app.add_middleware(NoOpAuthMiddleware)
    
    @app.get("/")
    async def index():
        return {"ok": True}
        
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
