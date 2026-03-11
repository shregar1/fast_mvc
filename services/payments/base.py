"""
Base abstractions for payment gateways.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CheckoutSession:
    """
    Represents a generic checkout session.
    """

    id: str
    url: Optional[str] = None
    provider: Optional[str] = None
    raw: Dict[str, Any] | None = None


class IPaymentGateway:
    """
    Base interface for payment gateway implementations.
    """

    name: str

    async def create_checkout_session(
        self,
        amount: int,
        currency: str,
        customer: Dict[str, Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> CheckoutSession:
        raise NotImplementedError

    async def capture_payment(self, payment_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def refund_payment(
        self,
        payment_id: str,
        amount: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        raise NotImplementedError

    async def verify_webhook(
        self,
        payload: bytes,
        headers: Dict[str, str],
    ) -> Dict[str, Any]:
        raise NotImplementedError

