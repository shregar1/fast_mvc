"""
High-level payment service that orchestrates multiple providers.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from loguru import logger

from configurations.payments import PaymentsConfiguration
from services.payments.base import CheckoutSession, IPaymentGateway
from services.payments.link import LinkGateway
from services.payments.paypal import PaypalGateway
from services.payments.payu import PayUGateway
from services.payments.razorpay import RazorpayGateway
from services.payments.stripe import StripeGateway


class PaymentService:
    """
    High-level payment service.

    Provides a unified interface to multiple payment gateways:
    Stripe, Razorpay, PayPal, PayU, and a generic Link provider.
    """

    def __init__(self) -> None:
        cfg = PaymentsConfiguration().get_config()
        self._gateways: Dict[str, IPaymentGateway] = {}

        self._gateways["stripe"] = StripeGateway()
        self._gateways["razorpay"] = RazorpayGateway()
        self._gateways["paypal"] = PaypalGateway()
        self._gateways["payu"] = PayUGateway()
        self._gateways["link"] = LinkGateway()

    def get_gateway(self, provider: str) -> Optional[IPaymentGateway]:
        """
        Get a gateway by provider name.
        """
        provider = provider.lower()
        gw = self._gateways.get(provider)
        if not gw:
            logger.warning("Requested unknown payment provider", provider=provider)
        return gw

    async def create_checkout(
        self,
        provider: str,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        """
        Create a checkout session using the given provider.
        """
        gateway = self.get_gateway(provider)
        if not gateway:
            return CheckoutSession(id="unknown_provider", provider=provider)

        return await gateway.create_checkout_session(
            amount=amount,
            currency=currency,
            customer=customer,
            metadata=metadata,
        )

    async def capture(
        self,
        provider: str,
        payment_id: str,
    ) -> Dict[str, Any]:
        gateway = self.get_gateway(provider)
        if not gateway:
            return {"provider": provider, "payment_id": payment_id, "status": "unknown_provider"}
        return await gateway.capture_payment(payment_id)

    async def refund(
        self,
        provider: str,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        gateway = self.get_gateway(provider)
        if not gateway:
            return {"provider": provider, "payment_id": payment_id, "status": "unknown_provider"}
        return await gateway.refund_payment(payment_id, amount=amount, reason=reason)

    async def verify_webhook(
        self,
        provider: str,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        gateway = self.get_gateway(provider)
        if not gateway:
            return {"provider": provider, "status": "unknown_provider"}
        return await gateway.verify_webhook(payload, headers)

