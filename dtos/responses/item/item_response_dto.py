"""Single item response DTO."""

from __future__ import annotations

from typing import Self

from dtos.responses.I import IResponseDTO


class ItemResponseDTO(IResponseDTO):
    """DTO for item responses."""

    transactionUrn: str = ""
    status: str = "SUCCESS"
    responseMessage: str = "Success"
    responseKey: str = "success"
    data: list | dict | None = None
    errors: list | dict | None = None
    id: str
    name: str
    description: str
    completed: bool
    created_at: str
    updated_at: str

    def to_dict(self) -> dict:
        out = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.reference_urn is not None:
            out["reference_urn"] = self.reference_urn
        return out

    @classmethod
    def from_entity(cls, entity, *, reference_urn: str | None = None) -> Self:
        return cls(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            completed=entity.completed,
            created_at=entity.created_at.isoformat(),
            updated_at=entity.updated_at.isoformat(),
            reference_urn=reference_urn,
        )
