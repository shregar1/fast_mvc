"""
DTOs for Slack / chat configuration settings.
"""

from typing import Optional

from pydantic import BaseModel


class SlackConfigurationDTO(BaseModel):
    """
    DTO for Slack configuration.

    Fields:
        enabled (bool): Whether Slack integration is enabled.
        webhook_url (str | None): Incoming webhook URL (classic Slack).
        bot_token (str | None): Bot token for Web API usage.
        default_channel (str | None): Default channel (e.g. "#alerts").
    """

    enabled: bool = False
    webhook_url: Optional[str] = None
    bot_token: Optional[str] = None
    default_channel: Optional[str] = None

