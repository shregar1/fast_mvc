"""Optional gRPC server support (health-first).

This keeps gRPC as an opt-in transport, aligned with FastX's configuration
and layered approach.

Currently implemented:
- gRPC server with a simple unary HealthService.Check RPC.

Future expansion:
- Add more gRPC services as separate vertical-slice modules.
- Reuse the same JWT auth configuration for gRPC interceptors.
"""

from __future__ import annotations

import time
from collections.abc import Iterable
from typing import Any, Callable, Optional

from loguru import logger

from constants.default import Default
from constants.environment import EnvironmentVar
from constants.http_header import HttpHeader
from utilities.env import EnvironmentParserUtility


GRPC_ERROR_MISSING_BEARER_TOKEN = "Missing Bearer token"
GRPC_ERROR_INVALID_TOKEN = "Invalid token"
GRPC_SHUTDOWN_GRACE_SECONDS = 5
GRPC_STATUS_ERROR = "ERROR"


def _extract_bearer_token(metadata: Iterable[tuple[str, Any]]) -> Optional[str]:
    for k, v in metadata:
        if str(k).lower() == HttpHeader.AUTHORIZATION.lower() and v is not None:
            s = str(v)
            if s.lower().startswith(HttpHeader.AUTHORIZATION_BEARER_PREFIX.lower()):
                return s.split(" ", 1)[1].strip()
    return None


async def start_grpc_health_server() -> Any:
    """Start the optional gRPC health server and return the aio server."""
    # Local imports so FastX works without grpc installed (until enabled).
    import grpc  # type: ignore

    from fastx.grpc.health.v1 import health_pb2, health_pb2_grpc
    from fastx.grpc.user.v1 import user_pb2, user_pb2_grpc

    jwt_enabled = EnvironmentParserUtility.get_bool_with_logging(
        EnvironmentVar.JWT_AUTH_ENABLED,
        Default.JWT_AUTH_ENABLED,
    )
    jwt_secret = EnvironmentParserUtility.parse_str(
        EnvironmentVar.SECRET_KEY,
        Default.SECRET_KEY,
    )
    jwt_algorithm = EnvironmentParserUtility.parse_str(
        EnvironmentVar.ALGORITHM,
        Default.ALGORITHM,
    )

    host = EnvironmentParserUtility.parse_str(EnvironmentVar.GRPC_HOST, Default.GRPC_HOST)
    port = EnvironmentParserUtility.parse_int(EnvironmentVar.GRPC_PORT, Default.GRPC_PORT)

    # Match FastAPI behavior: if JWT is enabled but secret isn't configured,
    # HTTP middleware is not registered. For gRPC, we also skip enforcement.
    jwt_enabled_effective = bool(jwt_enabled and jwt_secret.strip())
    if jwt_enabled and not jwt_secret.strip():
        logger.warning(
            "JWT_AUTH_ENABLED is true but SECRET_KEY is empty; gRPC JWT enforcement disabled."
        )

    jwt_decode: Optional[Callable[..., Any]] = None
    if jwt_enabled_effective:
        import jwt as _jwt  # pyjwt

        jwt_decode = _jwt.decode

    grpc_mod = grpc
    server = grpc_mod.aio.server()

    # Import DTO/service/repo once per server start to keep per-RPC overhead low.
    from dtos.responses.apis.v1.user.fetch import FetchUserResponseDataDTO
    from repositories.user.fetch import FetchUserRepository
    from services.user.fetch import FetchUserService
    fetch_service = FetchUserService(repo=FetchUserRepository())

    class _HealthServicer(health_pb2_grpc.HealthServiceServicer):
        async def Check(self, request: health_pb2.HealthRequest, context) -> Any:
            if jwt_enabled_effective:
                token = _extract_bearer_token(context.invocation_metadata())
                if not token:
                    await context.abort(
                        grpc_mod.StatusCode.UNAUTHENTICATED,
                        GRPC_ERROR_MISSING_BEARER_TOKEN,
                    )
                    return health_pb2.HealthResponse(
                        status=GRPC_STATUS_ERROR,
                        timestamp_unix_ms=0,
                        details=GRPC_ERROR_MISSING_BEARER_TOKEN,
                    )

                try:
                    assert jwt_decode is not None  # for type checkers
                    jwt_decode(token, jwt_secret, algorithms=[jwt_algorithm])
                except Exception:
                    await context.abort(
                        grpc_mod.StatusCode.UNAUTHENTICATED,
                        GRPC_ERROR_INVALID_TOKEN,
                    )
                    return health_pb2.HealthResponse(
                        status=GRPC_STATUS_ERROR,
                        timestamp_unix_ms=0,
                        details=GRPC_ERROR_INVALID_TOKEN,
                    )

            return health_pb2.HealthResponse(
                status="SERVING",
                timestamp_unix_ms=int(time.time() * 1000),
                details="gRPC health ok",
            )

    class _UserServicer(user_pb2_grpc.UserServiceServicer):
        async def FetchUser(
            self, request: user_pb2.FetchUserRequest, context
        ) -> Any:
            if jwt_enabled_effective:
                token = _extract_bearer_token(context.invocation_metadata())
                if not token:
                    await context.abort(
                        grpc_mod.StatusCode.UNAUTHENTICATED,
                        GRPC_ERROR_MISSING_BEARER_TOKEN,
                    )
                    return user_pb2.FetchUserResponse(
                        id="",
                        message=GRPC_ERROR_MISSING_BEARER_TOKEN,
                        status="",
                    )

                try:
                    assert jwt_decode is not None
                    jwt_decode(token, jwt_secret, algorithms=[jwt_algorithm])
                except Exception:
                    await context.abort(
                        grpc_mod.StatusCode.UNAUTHENTICATED,
                        GRPC_ERROR_INVALID_TOKEN,
                    )
                    return user_pb2.FetchUserResponse(
                        id="",
                        message=GRPC_ERROR_INVALID_TOKEN,
                        status="",
                    )

            # Your current Request DTOs are ABC-style interfaces (not instantiable
            # pydantic models). Pass a lightweight adapter with expected attributes.
            from types import SimpleNamespace

            name: str = getattr(request, "name", "")
            desc: str = getattr(request, "description", "")
            dto = SimpleNamespace(
                name=name,
                description=desc or None,
                reference_urn="",  # not available in this transport yet
            )

            result = fetch_service.run(dto)
            item = (result or {}).get("item") or {}
            user_id = str(item.get("id", "")) if item is not None else ""
            message = str((result or {}).get("message", ""))

            resp_data = FetchUserResponseDataDTO(id=user_id)
            return user_pb2.FetchUserResponse(
                id=user_id,
                message=message,
                status=resp_data.status,
            )

    health_pb2_grpc.add_HealthServiceServicer_to_server(_HealthServicer(), server)
    user_pb2_grpc.add_UserServiceServicer_to_server(_UserServicer(), server)

    bound_port = server.add_insecure_port(f"{host}:{port}")
    setattr(server, "_fastmvc_bound_port", bound_port)

    await server.start()
    logger.info(f"gRPC HealthService started on {host}:{bound_port}")
    return server


async def stop_grpc_server(server: Any, grace_seconds: int = GRPC_SHUTDOWN_GRACE_SECONDS) -> None:
    """Gracefully stop the aio gRPC server."""
    if server is None:
        return
    try:
        await server.stop(grace_seconds)
    except Exception:
        # Best-effort shutdown; don't crash app shutdown.
        logger.exception("Failed to stop gRPC server cleanly")

