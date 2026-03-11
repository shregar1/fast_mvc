"""
Payment services package.

Provides a high-level PaymentService and concrete gateway implementations
for Stripe, Razorpay, PayPal, PayU, and a generic Link provider.
"""

from services.payments.service import PaymentService

__all__ = ["PaymentService"]

