"""
Push notification service for iOS and Android.

This module defines a high-level service that can send notifications
via APNS (iOS) and FCM (Android). The concrete integrations are left
as TODOs so that projects can plug in their chosen SDKs.
"""

from typing import Any, Dict, List, Optional

from loguru import logger

from configurations.push import PushConfiguration


class PushNotificationService:
    """
    High-level push notification service.

    Reads configuration from `config/push/config.json` via PushConfiguration.
    """

    def __init__(self) -> None:
        cfg = PushConfiguration().get_config()
        self._apns = cfg.apns
        self._fcm = cfg.fcm

    @property
    def apns_enabled(self) -> bool:
        return bool(self._apns.enabled)

    @property
    def fcm_enabled(self) -> bool:
        return bool(self._fcm.enabled)

    async def send_to_ios(
        self,
        device_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Send a push notification to iOS devices via APNS.

        This is a placeholder that currently only logs the intent.
        Projects can replace this with a real APNS client (e.g. apns2).
        """
        if not self.apns_enabled:
            logger.warning("APNS push attempted but APNS is disabled in config.")
            return

        logger.info(
            "Sending APNS notification",
            device_tokens=device_tokens,
            title=title,
            body=body,
            data=data or {},
        )
        # TODO: Integrate with real APNS client library.

    async def send_to_android(
        self,
        registration_tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict[str, Any]] = None,
        topic: Optional[str] = None,
    ) -> None:
        """
        Send a push notification to Android devices via FCM.

        This is a placeholder that currently only logs the intent.
        Projects can replace this with a real FCM client (e.g. pyfcm).
        """
        if not self.fcm_enabled:
            logger.warning("FCM push attempted but FCM is disabled in config.")
            return

        logger.info(
            "Sending FCM notification",
            registration_tokens=registration_tokens,
            title=title,
            body=body,
            data=data or {},
            topic=topic,
        )
        # TODO: Integrate with real FCM client library.

