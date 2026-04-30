"""Repository-oriented FastAPI dependencies."""

from dependencies.repositories.abstraction import IRepositoryDependency
from dependencies.repositories.example import ExampleRepositoryDependency

__all__ = [
    "IRepositoryDependency",
    "ExampleRepositoryDependency",
]
