"""Request DTO Abstraction Module.

This module defines the I request DTO interface that all request
DTOs should inherit from.

Usage:
    >>> from dtos.requests.abstraction import IRequestDTO
    >>>
    >>> class MyRequestDTO(IRequestDTO):
    ...     custom_field: str

Note:
    The ``reference_number`` is passed via the ``X-Reference-Number``
    request header (not in the body).  The middleware extracts it and
    stores it on ``request.state.reference_number`` so controllers and
    response envelopes can echo it back automatically.
"""

from pydantic import BaseModel

from abstractions.dto import IDTO


class IRequestDTO(BaseModel, IDTO):
    """Abstract base for all request DTOs.

    Inherits :class:`abstractions.dto.IDTO`.

    Concrete request DTOs extend this class with their own fields.
    Client-side correlation is handled via the ``X-Reference-Number``
    request header — it is no longer part of the request body.
    """

    pass
