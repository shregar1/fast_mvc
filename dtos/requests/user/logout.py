"""Logout request DTO."""

from dtos.requests.user.abstraction import IRequestUserDTO


class UserLogoutRequestDTO(IRequestUserDTO):
    """DTO for POST /user/logout."""

    pass


__all__ = ["UserLogoutRequestDTO"]
