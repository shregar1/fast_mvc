"""
Generic pay-by-link gateway implementation.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from loguru import logger

from configurations.payments import PaymentsConfiguration
from services.payments.base import CheckoutSession, IPaymentGateway


class LinkGateway(IPaymentGateway):
    name = "link"

    def __init__(self) -> None:
        cfg = PaymentsConfiguration().get_config().link
        self._cfg = cfg

    @property
    def enabled(self) -> bool:
        return bool(self._cfg.enabled and self._cfg.base_url and self._cfg.api_key)

    async def create_checkout_session(
        self,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        if not self.enabled:
            logger.warning("LinkGateway.create_checkout_session called but Link is disabled.")
            return CheckoutSession(id="disabled", provider=self.name)

        try:
            import httpx  # type: ignore
        except Exception:  # pragma: no cover
            logger.error("httpx is required to use LinkGateway.")
            return CheckoutSession(id="error", provider=self.name)

        payload: Dict[str, Any] = {
            "amount": amount,
            "currency": currency,
            "customer": customer or {},
            "metadata": metadata or {},
        }
        headers = {
            "Authorization": f"Bearer {self._cfg.api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._cfg.base_url.rstrip('/')}/checkout-links",
                json=payload,
                headers=headers,
            )
        if resp.status_code >= 300:
            logger.error("Link checkout creation failed", status_code=resp.status_code, body=resp.text)
            return CheckoutSession(id="error", provider=self.name, raw={"status": resp.status_code})

        data = resp.json()
        return CheckoutSession(
            id=data.get("id", ""),
            url=data.get("url"),
            provider=self.name,
            raw=data,
        )

    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        logger.info("Link capture_payment invoked", payment_id=payment_id)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("Link refund_payment invoked", payment_id=payment_id, amount=amount, reason=reason)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def verify_webhook(
        self,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        logger.info("Link verify_webhook invoked")
        try:
            data = json.loads(payload.decode("utf-8"))
        except Exception:
            data = {}
        return {"provider": self.name, "payload": data, "status": "unverified"}

