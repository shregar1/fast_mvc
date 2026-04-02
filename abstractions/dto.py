"""HTTP DTO contracts for the application layer.

These abstract markers anchor :mod:`dtos` request, response, and configuration models to the
:mod:`abstractions` package so layered DTOs form an explicit inheritance
chain. All concrete Pydantic DTOs participate in :class:`IDTO`. Request bases
live under :mod:`dtos.requests` (e.g. :class:`dtos.requests.abstraction.IRequestDTO`).
"""

from abc import ABC


class IDTO(ABC):
    """Root marker for all Data Transfer Objects in :mod:`dtos`.

    Concrete models combine :class:`IDTO` with :class:`pydantic.BaseModel` or
    :class:`dtos.base.ApplicationBaseModel` — for example :class:`dtos.configuration.abstraction.IConfigurationDTO`
    or :class:`dtos.requests.abstraction.IRequestDTO` for HTTP requests.
    """
