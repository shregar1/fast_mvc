"""Application core integration layer (FastAPI wiring, optional services).

This module provides re-exports for optional fastx_platform services.
Each import is wrapped in try/except to allow the core to work without
the optional dependencies.

Usage:
    # Core only (no optional dependencies)
    from core import app

    # With optional services (requires fast-platform)
    from core import CircuitBreaker, Metrics
"""

# Optional fastx_platform services - gracefully degrade if not installed
# These require: pip install fastx-mvc[platform] or specific extras

# Observability (fastx_platform.observability)
try:
    from fastx_platform.observability import AuditLog, Metrics, StructuredLogger, Tracer
except ImportError:
    AuditLog = None  # type: ignore
    Metrics = None  # type: ignore
    StructuredLogger = None  # type: ignore
    Tracer = None  # type: ignore

# Tasks/Jobs (fastx_platform.jobs)
try:
    from core.tasks import (
        JobsConfiguration,
        JobsConfigurationDTO,
        cancel_job,
        enqueue,
        get_job_status,
    )
except ImportError:
    JobsConfiguration = None  # type: ignore
    JobsConfigurationDTO = None  # type: ignore
    cancel_job = None  # type: ignore
    enqueue = None  # type: ignore
    get_job_status = None  # type: ignore

# Security (fastx_platform.security)
try:
    from core.security import APIKeyManager, FieldEncryption, WebhookVerifier
except ImportError:
    APIKeyManager = None  # type: ignore
    FieldEncryption = None  # type: ignore
    WebhookVerifier = None  # type: ignore

# Feature Flags (fastx_platform.features)
try:
    from core.features import FeatureFlags, feature_flag
except ImportError:
    FeatureFlags = None  # type: ignore
    feature_flag = None  # type: ignore

# Tenancy (fastx_platform.tenancy)
try:
    from core.tenancy import Tenant, TenantContext, get_current_tenant
except ImportError:
    Tenant = None  # type: ignore
    TenantContext = None  # type: ignore
    get_current_tenant = None  # type: ignore

# Versioning (fastx_platform.utils.versioning)
try:
    from fastx_platform.utils.versioning import APIVersion, versioned_router
except ImportError:
    APIVersion = None  # type: ignore
    versioned_router = None  # type: ignore


__all__ = [
    # Observability
    "StructuredLogger",
    "Metrics",
    "Tracer",
    "AuditLog",
    # Jobs (fastx_jobs)
    "enqueue",
    "cancel_job",
    "get_job_status",
    "JobsConfiguration",
    "JobsConfigurationDTO",
    # Security
    "APIKeyManager",
    "WebhookVerifier",
    "FieldEncryption",
    # Features
    "FeatureFlags",
    "feature_flag",
    # Tenancy (fastx_tenancy)
    "Tenant",
    "TenantContext",
    "get_current_tenant",
    # Versioning
    "APIVersion",
    "versioned_router",
]
