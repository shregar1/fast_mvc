"""FastX - Minimal Core Framework.

A production-grade MVC framework for FastAPI with clean architecture,
dependency injection, and modular service integration.

Basic Usage:
    from fastx_mvc import FastXApp, Controller, Service, Repository

    app = FastXApp()
    app.run()

With Optional Services:
    # Install: pip install fastx-mvc[platform]
    from fastx_platform.notifications import EmailClient
    from fastx_platform.storage import S3Client

Modules:
    - abstractions: I interfaces (Controller, Service, Repository, etc.)
    - dtos: Data Transfer Objects and validation
    - dependencies: DI container and utilities
    - models, services, repositories: domain layers

Optional Integrations (via fastx-platform):
    - notifications: Email, SMS, Chat, Push notifications
    - storage: S3, GCS, Azure Blob
    - messaging: SQS, Pub/Sub, Service Bus
    - payments: Stripe integration
    - observability: Monitoring, tracing, logging
    - llm: AI/LLM integrations
    - search: Full-text search
    - resilience: Circuit breakers, retries
"""

# Core abstractions
from abstractions.controller import IController
from abstractions.service import IService
from abstractions.repository import IRepository
from abstractions.entity import Entity, IEntity, AggregateRoot, IAggregateRoot
from abstractions.unit_of_work import IUnitOfWork, IUnitOfWork
from abstractions.result import Result, Success, Failure, success, failure

# DTOs
from dtos.responses.abstraction import IResponseDTO
from dtos.requests.abstraction import IRequestDTO

# Application factory
from app import app as FastXApp


__version__ = "1.5.0"

__all__ = [
    # Version
    "__version__",
    # Core abstractions
    "IController",
    "IService",
    "IRepository",
    "Entity",
    "IEntity",
    "AggregateRoot",
    "IAggregateRoot",
    "IUnitOfWork",
    "IUnitOfWork",
    # Result pattern
    "Result",
    "Success",
    "Failure",
    "success",
    "failure",
    # DTOs
    "IResponseDTO",
    "IRequestDTO",
    # App
    "FastXApp",
]

