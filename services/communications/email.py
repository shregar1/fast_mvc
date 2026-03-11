"""
High-level email service.

Supports SMTP and SendGrid backends, configured via
`config/email/config.json` and exposed through EmailConfiguration.

This is intentionally lightweight: it covers the 80% use case of
sending structured emails from services and controllers while
allowing projects to extend or replace the implementation.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Iterable, Optional

from loguru import logger

from configurations.email import EmailConfiguration


class EmailService:
    """
    High-level email sending service.

    Usage:

        email_service = EmailService()
        await email_service.send_email(
            to=["user@example.com"],
            subject="Welcome",
            body="Thanks for signing up.",
        )
    """

    def __init__(self) -> None:
        cfg = EmailConfiguration().get_config()
        self._smtp_cfg = cfg.smtp
        self._sendgrid_cfg = cfg.sendgrid

    @property
    def smtp_enabled(self) -> bool:
        return bool(self._smtp_cfg.enabled)

    @property
    def sendgrid_enabled(self) -> bool:
        return bool(self._sendgrid_cfg.enabled and self._sendgrid_cfg.api_key)

    async def send_email(
        self,
        to: Iterable[str],
        subject: str,
        body: str,
        html_body: Optional[str] = None,
        from_address: Optional[str] = None,
    ) -> None:
        """
        Send an email using the first enabled backend (SendGrid preferred, then SMTP).
        """
        recipients = list(to)
        if not recipients:
            logger.warning("EmailService.send_email called with no recipients.")
            return

        if self.sendgrid_enabled:
            await self._send_via_sendgrid(
                to=recipients,
                subject=subject,
                body=body,
                html_body=html_body,
                from_address=from_address,
            )
            return

        if self.smtp_enabled:
            await self._send_via_smtp(
                to=recipients,
                subject=subject,
                body=body,
                html_body=html_body,
                from_address=from_address,
            )
            return

        logger.warning("EmailService has no enabled backend; email dropped.")

    async def _send_via_smtp(
        self,
        to: list[str],
        subject: str,
        body: str,
        html_body: Optional[str],
        from_address: Optional[str],
    ) -> None:
        cfg = self._smtp_cfg
        sender = from_address or cfg.default_from or (cfg.username or "no-reply@example.com")

        msg = EmailMessage()
        msg["From"] = sender
        msg["To"] = ", ".join(to)
        msg["Subject"] = subject
        if html_body:
            msg.set_content(body or "")
            msg.add_alternative(html_body, subtype="html")
        else:
            msg.set_content(body or "")

        logger.info(
            "Sending email via SMTP",
            host=cfg.host,
            port=cfg.port,
            use_tls=cfg.use_tls,
            use_ssl=cfg.use_ssl,
            from_address=sender,
            to=to,
        )

        try:
            if cfg.use_ssl:
                smtp = smtplib.SMTP_SSL(cfg.host, cfg.port)
            else:
                smtp = smtplib.SMTP(cfg.host, cfg.port)

            with smtp as client:
                client.ehlo()
                if cfg.use_tls and not cfg.use_ssl:
                    client.starttls()
                    client.ehlo()
                if cfg.username and cfg.password:
                    client.login(cfg.username, cfg.password)
                client.send_message(msg)
        except Exception as exc:  # pragma: no cover - network dependent
            logger.error(f"SMTP email send failed: {exc}")

    async def _send_via_sendgrid(
        self,
        to: list[str],
        subject: str,
        body: str,
        html_body: Optional[str],
        from_address: Optional[str],
    ) -> None:
        cfg = self._sendgrid_cfg
        api_key = cfg.api_key
        if not api_key:
            logger.warning("SendGrid enabled but API key is missing.")
            return

        sender = from_address or cfg.default_from or "no-reply@example.com"
        logger.info(
            "Sending email via SendGrid",
            from_address=sender,
            to=to,
        )

        try:
            import httpx  # type: ignore

            payload = {
                "personalizations": [{"to": [{"email": addr} for addr in to]}],
                "from": {"email": sender},
                "subject": subject,
                "content": [
                    {
                        "type": "text/plain" if not html_body else "text/html",
                        "value": html_body or body or "",
                    }
                ],
            }

            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(
                    "https://api.sendgrid.com/v3/mail/send",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                )
            if resp.status_code >= 300:
                logger.error(
                    "SendGrid email send failed",
                    status_code=resp.status_code,
                    body=resp.text,
                )
        except Exception as exc:  # pragma: no cover - network dependent
            logger.error(f"SendGrid email send failed: {exc}")

