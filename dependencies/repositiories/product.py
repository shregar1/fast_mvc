"""
Product Repository Dependency.

Provides dependency injection for ProductRepository.
"""

from sqlalchemy.orm import Session

from abstractions.dependency import IDependency
from fast_database.persistence.repositories.product import ProductRepository


class ProductRepositoryDependency(IDependency):
    """Dependency provider for ProductRepository."""

    @staticmethod
    def derive(session: Session) -> ProductRepository:
        """
        Create repository instance with session.

        Args:
            session: SQLAlchemy session.

        Returns:
            Configured ProductRepository.
        """
        repo = ProductRepository()
        repo.session = session
        return repo
