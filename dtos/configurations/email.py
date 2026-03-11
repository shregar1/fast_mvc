"""
DTOs for email provider configuration settings.
"""

from typing import Optional

from pydantic import BaseModel


class SMTPConfigDTO(BaseModel):
    """
    Configuration for a traditional SMTP relay.
    """

    enabled: bool = False
    host: str = "localhost"
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    use_tls: bool = True
    use_ssl: bool = False
    default_from: Optional[str] = None


class SendGridConfigDTO(BaseModel):
    """
    Configuration for SendGrid HTTP API.
    """

    enabled: bool = False
    api_key: Optional[str] = None
    default_from: Optional[str] = None


class EmailConfigurationDTO(BaseModel):
    """
    Complete email configuration DTO.

    Supports both SMTP and SendGrid; projects can enable one or both.
    """

    smtp: SMTPConfigDTO = SMTPConfigDTO()
    sendgrid: SendGridConfigDTO = SendGridConfigDTO()

