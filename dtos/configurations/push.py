"""
DTOs for push notification configuration (iOS/Android).
"""

from typing import List, Optional

from pydantic import BaseModel


class APNSConfigDTO(BaseModel):
    """Apple Push Notification Service configuration."""

    enabled: bool = False
    key_id: Optional[str] = None
    team_id: Optional[str] = None
    bundle_id: Optional[str] = None
    private_key_path: Optional[str] = None
    use_sandbox: bool = True


class FCMConfigDTO(BaseModel):
    """Firebase Cloud Messaging configuration."""

    enabled: bool = False
    server_key: Optional[str] = None
    project_id: Optional[str] = None
    default_topics: List[str] = []


class PushConfigurationDTO(BaseModel):
    """
    Complete push notification configuration DTO.

    Contains APNS and FCM sections.
    """

    apns: APNSConfigDTO = APNSConfigDTO()
    fcm: FCMConfigDTO = FCMConfigDTO()

