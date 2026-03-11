"""
Email Configuration Module.

Provides a singleton configuration manager for email provider settings
(SMTP and SendGrid).
"""

import json
from typing import Optional

from dtos.configurations.email import EmailConfigurationDTO, SMTPConfigDTO, SendGridConfigDTO
from start_utils import logger


class EmailConfiguration:
    """
    Singleton configuration manager for email settings.

    Configuration is loaded from `config/email/config.json`.
    """

    _instance: Optional["EmailConfiguration"] = None

    def __new__(cls) -> "EmailConfiguration":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance.load_config()
        return cls._instance

    def load_config(self) -> None:
        """
        Load email configuration from JSON file.
        """
        try:
            with open("config/email/config.json") as file:
                self.config = json.load(file)
            logger.debug("Email config loaded successfully.")
        except FileNotFoundError:
            logger.debug("Email config file not found.")
            self.config = {}
        except json.JSONDecodeError:
            logger.debug("Error decoding email config file.")
            self.config = {}

    def get_config(self) -> EmailConfigurationDTO:
        """
        Get unified email configuration as a validated DTO.
        """
        smtp_raw = self.config.get("smtp", {}) or {}
        sendgrid_raw = self.config.get("sendgrid", {}) or {}

        smtp = SMTPConfigDTO(
            enabled=bool(smtp_raw.get("enabled", False)),
            host=smtp_raw.get("host", "localhost"),
            port=int(smtp_raw.get("port", 587)),
            username=smtp_raw.get("username"),
            password=smtp_raw.get("password"),
            use_tls=bool(smtp_raw.get("use_tls", True)),
            use_ssl=bool(smtp_raw.get("use_ssl", False)),
            default_from=smtp_raw.get("default_from"),
        )
        sendgrid = SendGridConfigDTO(
            enabled=bool(sendgrid_raw.get("enabled", False)),
            api_key=sendgrid_raw.get("api_key"),
            default_from=sendgrid_raw.get("default_from"),
        )
        return EmailConfigurationDTO(smtp=smtp, sendgrid=sendgrid)

