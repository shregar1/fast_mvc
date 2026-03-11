"""
PayPal payment gateway implementation (REST API skeleton).
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from loguru import logger

from configurations.payments import PaymentsConfiguration
from services.payments.base import CheckoutSession, IPaymentGateway


class PaypalGateway(IPaymentGateway):
    name = "paypal"

    def __init__(self) -> None:
        cfg = PaymentsConfiguration().get_config().paypal
        self._cfg = cfg

    @property
    def enabled(self) -> bool:
        return bool(self._cfg.enabled and self._cfg.client_id and self._cfg.client_secret)

    def _base_url(self) -> str:
        if self._cfg.environment == "live":
            return "https://api-m.paypal.com"
        return "https://api-m.sandbox.paypal.com"

    async def _get_access_token(self) -> Optional[str]:
        try:
            import httpx  # type: ignore
        except Exception:  # pragma: no cover
            logger.error("httpx is required to use PaypalGateway.")
            return None

        auth = (self._cfg.client_id or "", self._cfg.client_secret or "")
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._base_url()}/v1/oauth2/token",
                data={"grant_type": "client_credentials"},
                auth=auth,
            )
        if resp.status_code >= 300:
            logger.error("PayPal OAuth failed", status_code=resp.status_code, body=resp.text)
            return None
        return resp.json().get("access_token")

    async def create_checkout_session(
        self,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        if not self.enabled:
            logger.warning("PaypalGateway.create_checkout_session called but PayPal is disabled.")
            return CheckoutSession(id="disabled", provider=self.name)

        token = await self._get_access_token()
        if not token:
            return CheckoutSession(id="error", provider=self.name)

        try:
            import httpx  # type: ignore
        except Exception:  # pragma: no cover
            logger.error("httpx is required to use PaypalGateway.")
            return CheckoutSession(id="error", provider=self.name)

        payload: Dict[str, Any] = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": (currency or "USD").upper(),
                        "value": f"{amount/100:.2f}",
                    }
                }
            ],
        }
        if metadata:
            payload["custom_id"] = metadata.get("orderId")

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{self._base_url()}/v2/checkout/orders",
                json=payload,
                headers=headers,
            )
        if resp.status_code >= 300:
            logger.error("PayPal order creation failed", status_code=resp.status_code, body=resp.text)
            return CheckoutSession(id="error", provider=self.name, raw={"status": resp.status_code})

        data = resp.json()
        approve_url = None
        for link in data.get("links", []):
            if link.get("rel") == "approve":
                approve_url = link.get("href")
                break

        return CheckoutSession(
            id=data.get("id", ""),
            url=approve_url,
            provider=self.name,
            raw=data,
        )

    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        logger.info("PayPal capture_payment invoked", payment_id=payment_id)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("PayPal refund_payment invoked", payment_id=payment_id, amount=amount, reason=reason)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def verify_webhook(
        self,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        logger.info("PayPal verify_webhook invoked")
        try:
            data = json.loads(payload.decode("utf-8"))
        except Exception:
            data = {}
        return {"provider": self.name, "payload": data, "status": "unverified"}

