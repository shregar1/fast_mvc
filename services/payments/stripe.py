"""
Stripe payment gateway implementation.

This implementation is intentionally lightweight and uses the REST API
via httpx. Projects can swap it for the official stripe SDK if desired.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from loguru import logger

from configurations.payments import PaymentsConfiguration
from services.payments.base import CheckoutSession, IPaymentGateway


class StripeGateway(IPaymentGateway):
    name = "stripe"

    def __init__(self) -> None:
        cfg = PaymentsConfiguration().get_config().stripe
        self._cfg = cfg

    @property
    def enabled(self) -> bool:
        return bool(self._cfg.enabled and self._cfg.api_key)

    async def create_checkout_session(
        self,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        if not self.enabled:
            logger.warning("StripeGateway.create_checkout_session called but Stripe is disabled.")
            return CheckoutSession(id="disabled", url=None, provider=self.name)

        try:
            import httpx  # type: ignore
        except Exception:  # pragma: no cover
            logger.error("httpx is required to use StripeGateway.")
            return CheckoutSession(id="error", url=None, provider=self.name)

        payload: Dict[str, Any] = {
            "mode": "payment",
            "success_url": "https://example.com/success",
            "cancel_url": "https://example.com/cancel",
            "line_items": [
                {
                    "price_data": {
                        "currency": currency or self._cfg.default_currency,
                        "product_data": {"name": metadata.get("description", "Payment") if metadata else "Payment"},
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ],
        }
        if metadata:
            payload["metadata"] = metadata

        headers = {
            "Authorization": f"Bearer {self._cfg.api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Encode payload as form data
        def _flatten(data: Dict[str, Any], prefix: str = "") -> Dict[str, str]:
            flat: Dict[str, str] = {}
            for key, value in data.items():
                full_key = f"{prefix}{key}" if not prefix else f"{prefix}[{key}]"
                if isinstance(value, dict):
                    flat.update(_flatten(value, full_key))
                elif isinstance(value, list):
                    for idx, item in enumerate(value):
                        if isinstance(item, dict):
                            flat.update(_flatten(item, f"{full_key}[{idx}]"))
                        else:
                            flat[f"{full_key}[{idx}]"] = str(item)
                else:
                    flat[full_key] = str(value)
            return flat

        form = _flatten(payload)

        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                "https://api.stripe.com/v1/checkout/sessions",
                data=form,
                headers=headers,
            )
        if resp.status_code >= 300:
            logger.error("Stripe checkout session creation failed", status_code=resp.status_code, body=resp.text)
            return CheckoutSession(id="error", url=None, provider=self.name, raw={"status": resp.status_code})

        data = resp.json()
        return CheckoutSession(
            id=data.get("id", ""),
            url=data.get("url"),
            provider=self.name,
            raw=data,
        )

    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        logger.info("Stripe capture_payment invoked", payment_id=payment_id)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("Stripe refund_payment invoked", payment_id=payment_id, amount=amount, reason=reason)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def verify_webhook(
        self,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        logger.info("Stripe verify_webhook invoked")
        try:
            data = json.loads(payload.decode("utf-8"))
        except Exception:
            data = {}
        return {"provider": self.name, "payload": data, "status": "unverified"}

