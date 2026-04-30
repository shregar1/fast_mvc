"""Smoke-test every HTTP operation declared in OpenAPI (no uncaught 500s)."""

from __future__ import annotations

import re
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _substitute_path_params(path: str, parameters: list[dict[str, Any]] | None) -> str:
    """Replace ``{name}`` segments using OpenAPI parameter schemas when present."""
    if not parameters:
        return path
    by_name: dict[str, dict[str, Any]] = {
        p["name"]: p for p in parameters if p.get("in") == "path"
    }

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        schema = by_name.get(name, {}).get("schema", {})
        typ = schema.get("type")
        fmt = schema.get("format")
        if typ == "integer":
            return "1"
        if typ == "number":
            return "1.0"
        if typ == "boolean":
            return "true"
        if fmt == "uuid":
            return "00000000-0000-0000-0000-000000000001"
        return "00000000-0000-0000-0000-000000000001"

    return re.sub(r"\{([^}]+)\}", repl, path)


def _request_body_stub(op: dict[str, Any]) -> dict[str, Any] | None:
    """Minimal JSON object so FastAPI runs the route (may still return 422)."""
    rb = op.get("requestBody")
    if not rb:
        return None
    content = rb.get("content") or {}
    if "application/json" not in content:
        return None
    return {}


@pytest.mark.api
def test_openapi_every_route_returns_without_server_error(client: TestClient) -> None:
    """Hit each OpenAPI path/method; expect anything except 5xx."""
    r = client.get("/openapi.json")
    assert r.status_code == 200, r.text
    spec = r.json()
    paths: dict[str, Any] = spec.get("paths") or {}

    for path, path_item in paths.items():
        for method in ("get", "post", "put", "patch", "delete", "head", "options"):
            if method not in path_item:
                continue
            op = path_item[method]
            if op.get("deprecated"):
                continue

            url = _substitute_path_params(path, op.get("parameters"))
            kwargs: dict[str, Any] = {}
            body = _request_body_stub(op)
            if body is not None:
                kwargs["json"] = body

            resp = client.request(method.upper(), url, **kwargs)
            assert resp.status_code < 500, (
                f"{method.upper()} {url} -> {resp.status_code}: {resp.text[:500]}"
            )
