"""Configuration DTOs — typed settings for middleware and app wiring.

All concrete models inherit from :class:`IConfigurationDTO`.
"""

from dtos.configuration.abstraction import IConfigurationDTO
from dtos.configuration.cors import CorsSettingsDTO
from dtos.configuration.security_headers import (
    SecurityHeadersDefaults,
    SecurityHeadersSettingsDTO,
)

__all__ = [
    "CorsSettingsDTO",
    "IConfigurationDTO",
    "SecurityHeadersDefaults",
    "SecurityHeadersSettingsDTO",
]
