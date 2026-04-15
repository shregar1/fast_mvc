"""Concrete User repository – extends IUserRepository with domain finders."""

from __future__ import annotations

from typing import Any, Optional

from repositories.user.abstraction import IUserRepository


class UserRepository(IUserRepository):
    """Repository for the ``users`` table."""

    def __init__(
        self,
        urn: Optional[str] = None,
        user_urn: Optional[str] = None,
        api_name: Optional[str] = None,
        user_id: Optional[int] = None,
        session: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            urn=urn,
            user_urn=user_urn,
            api_name=api_name,
            user_id=user_id,
            session=session,
            *args,
            **kwargs,
        )
        self.session = session
        try:
            from fast_database.persistence.models.user import User
            self._model = User
        except ImportError:
            self._model = None

    @property
    def model(self):
        return self._model

    # ── Domain finders ──────────────────────────────────────────────

    def retrieve_record_by_email(
        self, email: str, is_deleted: bool = False
    ) -> Any | None:
        """Look up a user by email address."""
        if self.session is None or self._model is None:
            return None
        query = self.session.query(self._model).filter(
            self._model.email == email,
            self._model.is_deleted == is_deleted,
        )
        return query.first()

    def retrieve_record_by_phone(self, phone: str) -> Any | None:
        """Look up a user by phone number."""
        if self.session is None or self._model is None:
            return None
        return (
            self.session.query(self._model)
            .filter(self._model.phone == phone, self._model.is_deleted == False)
            .first()
        )

    def create_record(self, data: dict | Any) -> Any:
        """Create a new user record.

        Accepts either a dict (controller convenience) or a model instance.
        """
        if self.session is None or self._model is None:
            raise RuntimeError("Database session is required to create records.")

        if isinstance(data, dict):
            record = self._model(**data)
        else:
            record = data

        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def retrieve_record_by_id(self, id: str | int, is_deleted: bool = False) -> Any | None:
        """Look up a user by primary key."""
        if self.session is None or self._model is None:
            return None
        return (
            self.session.query(self._model)
            .filter(self._model.id == int(id), self._model.is_deleted == is_deleted)
            .first()
        )


__all__ = ["UserRepository"]
