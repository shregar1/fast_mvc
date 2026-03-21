"""
Example Repository.

This module provides data access operations for Example entities.
"""


from loguru import logger
from sqlalchemy.orm import Session

from abstractions.repository import IRepository
from fastmvc_db_models.example import Example


class ExampleRepository(IRepository):
    """
    Repository for Example database operations.

    Provides CRUD operations and queries for Example entities.

    Attributes:
        session (Session): SQLAlchemy database session.
    """

    def __init__(self, session: Session = None):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session instance.
        """
        self._session = session
        self.logger = logger.bind(repository="ExampleRepository")

    @property
    def session(self) -> Session:
        return self._session

    @session.setter
    def session(self, value: Session):
        self._session = value

    def create_record(self, record: Example) -> Example:
        """
        Create a new Example record.

        Args:
            record: Example instance to create.

        Returns:
            Created Example with generated ID.
        """
        self.logger.debug(f"Creating Example: {record.name}")
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        self.logger.info(f"Created Example with ID: {record.id}")
        return record

    def retrieve_record_by_id(self, record_id: int) -> Example | None:
        """
        Retrieve a Example by ID.

        Args:
            record_id: Example ID.

        Returns:
            Example instance or None if not found.
        """
        self.logger.debug(f"Retrieving Example by ID: {record_id}")
        return (
            self.session.query(Example)
            .filter(Example.id == record_id)
            .filter(not Example.is_deleted)
            .first()
        )

    def retrieve_record_by_urn(self, urn: str) -> Example | None:
        """
        Retrieve a Example by URN.

        Args:
            urn: Example URN.

        Returns:
            Example instance or None if not found.
        """
        self.logger.debug(f"Retrieving Example by URN: {urn}")
        return (
            self.session.query(Example)
            .filter(Example.urn == urn)
            .filter(not Example.is_deleted)
            .first()
        )

    def retrieve_all_records(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True,
    ) -> list[Example]:
        """
        Retrieve all Examples with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum records to return.
            active_only: Only return active records.

        Returns:
            List of Example instances.
        """
        self.logger.debug(f"Retrieving Examples: skip={skip}, limit={limit}")
        query = self.session.query(Example).filter(not Example.is_deleted)

        if active_only:
            query = query.filter(Example.is_active)

        return query.offset(skip).limit(limit).all()

    def update_record(self, record: Example) -> Example:
        """
        Update an existing Example record.

        Args:
            record: Example instance with updated values.

        Returns:
            Updated Example instance.
        """
        self.logger.debug(f"Updating Example: {record.id}")
        self.session.commit()
        self.session.refresh(record)
        self.logger.info(f"Updated Example: {record.id}")
        return record

    def delete_record(self, record_id: int, deleted_by: int) -> bool:
        """
        Soft delete a Example record.

        Args:
            record_id: Example ID to delete.
            deleted_by: ID of user performing deletion.

        Returns:
            True if deleted, False if not found.
        """
        self.logger.debug(f"Deleting Example: {record_id}")
        record = self.retrieve_record_by_id(record_id)

        if not record:
            return False

        record.is_deleted = True
        record.updated_by = deleted_by
        self.session.commit()
        self.logger.info(f"Soft deleted Example: {record_id}")
        return True

    def count_records(self, active_only: bool = True) -> int:
        """
        Count total Example records.

        Args:
            active_only: Only count active records.

        Returns:
            Total count.
        """
        query = self.session.query(Example).filter(not Example.is_deleted)

        if active_only:
            query = query.filter(Example.is_active)

        return query.count()
