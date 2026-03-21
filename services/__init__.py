"""
Services Package.

This package contains the business logic layer of the FastMVC application.
Services implement domain operations, coordinate between repositories and
external systems, and return structured responses.

Subpackages:
    - user/: User authentication and management services
    - product/: Example CRUD service
    - streams/: Market data hub for WebSocket demos (optional ``fastmvc_queues`` fan-out)
    - events/: Cloud event bus helpers used by streams

Integrations (payments, storage, vectors, search, etc.) use the published ``fastmvc_*``
packages — see pyproject optional-dependencies.

Usage:
    >>> from services.user.login import UserLoginService
    >>> from services.user.registration import UserRegistrationService
"""

