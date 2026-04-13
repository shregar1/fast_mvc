"""User-domain request DTO abstraction."""

from dtos.requests.abstraction import IRequestDTO


class IRequestUserDTO(IRequestDTO):
    """Interface for user-scoped request DTOs."""

    pass


__all__ = ["IRequestUserDTO"]
