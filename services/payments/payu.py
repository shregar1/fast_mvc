"""
PayU payment gateway implementation (skeleton).
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from loguru import logger

from configurations.payments import PaymentsConfiguration
from services.payments.base import CheckoutSession, IPaymentGateway


class PayUGateway(IPaymentGateway):
    name = "payu"

    def __init__(self) -> None:
        cfg = PaymentsConfiguration().get_config().payu
        self._cfg = cfg

    @property
    def enabled(self) -> bool:
        return bool(self._cfg.enabled and self._cfg.merchant_key and self._cfg.merchant_salt)

    async def create_checkout_session(
        self,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        if not self.enabled:
            logger.warning("PayUGateway.create_checkout_session called but PayU is disabled.")
            return CheckoutSession(id="disabled", provider=self.name)

        # Real PayU integration would construct a hash and redirect URL.
        # Here we simply return a placeholder session.
        logger.info("PayUGateway.create_checkout_session placeholder invoked", amount=amount, currency=currency)
        return CheckoutSession(
            id="payu-session-placeholder",
            url=None,
            provider=self.name,
            raw={"message": "PayU integration not fully implemented"},
        )

    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        logger.info("PayU capture_payment invoked", payment_id=payment_id)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("PayU refund_payment invoked", payment_id=payment_id, amount=amount, reason=reason)
        return {"provider": self.name, "payment_id": payment_id, "status": "not_implemented"}

    async def verify_webhook(
        self,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        logger.info("PayU verify_webhook invoked")
        try:
            data = json.loads(payload.decode("utf-8"))
        except Exception:
            data = {}
        return {"provider": self.name, "payload": data, "status": "unverified"}

