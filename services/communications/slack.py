"""
Slack chat / notification service.

Supports sending messages via either an incoming webhook or the Slack Web API
using a bot token, depending on what is configured.
"""

from __future__ import annotations

from typing import Iterable, Optional

from loguru import logger

from configurations.slack import SlackConfiguration


class SlackService:
    """
    High-level Slack messaging service.

    Usage:

        slack = SlackService()
        await slack.post_message(text="Deployed! ✅")
    """

    def __init__(self) -> None:
        cfg = SlackConfiguration().get_config()
        self._cfg = cfg

    @property
    def enabled(self) -> bool:
        return bool(self._cfg.enabled)

    async def post_message(
        self,
        text: str,
        channel: Optional[str] = None,
        blocks: Optional[Iterable[dict]] = None,
    ) -> None:
        """
        Post a message to Slack using the configured backend.
        """
        if not self.enabled:
            logger.warning("SlackService.post_message called but Slack is disabled in config.")
            return

        if self._cfg.webhook_url:
            await self._post_via_webhook(text=text, blocks=blocks)
            return

        if self._cfg.bot_token:
            await self._post_via_web_api(text=text, channel=channel, blocks=blocks)
            return

        logger.warning(
            "SlackService is enabled but neither webhook_url nor bot_token is configured."
        )

    async def _post_via_webhook(
        self,
        text: str,
        blocks: Optional[Iterable[dict]],
    ) -> None:
        import httpx  # type: ignore

        payload: dict = {"text": text}
        if blocks:
            payload["blocks"] = list(blocks)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(self._cfg.webhook_url or "", json=payload)
            if resp.status_code >= 300:
                logger.error(
                    "Slack webhook send failed",
                    status_code=resp.status_code,
                    body=resp.text,
                )
        except Exception as exc:  # pragma: no cover - network dependent
            logger.error(f"Slack webhook send failed: {exc}")

    async def _post_via_web_api(
        self,
        text: str,
        channel: Optional[str],
        blocks: Optional[Iterable[dict]],
    ) -> None:
        import httpx  # type: ignore

        token = self._cfg.bot_token
        if not token:
            logger.warning("Slack bot_token not configured.")
            return

        target_channel = channel or self._cfg.default_channel
        if not target_channel:
            logger.warning("Slack post attempted without a target channel.")
            return

        payload: dict = {"channel": target_channel, "text": text}
        if blocks:
            payload["blocks"] = list(blocks)

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    "https://slack.com/api/chat.postMessage",
                    json=payload,
                    headers={"Authorization": f"Bearer {token}"},
                )
            data = resp.json()
            if not data.get("ok"):
                logger.error("Slack API send failed", response=data)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.error(f"Slack API send failed: {exc}")

