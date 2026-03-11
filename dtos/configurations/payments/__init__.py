"""
Payment provider DTO package.

Splits each provider into its own module while still exposing a unified
`PaymentsConfigurationDTO` type for configuration aggregation.
"""

from dtos.configurations.payments.stripe import StripeConfigDTO
from dtos.configurations.payments.razorpay import RazorpayConfigDTO
from dtos.configurations.payments.paypal import PaypalConfigDTO
from dtos.configurations.payments.payu import PayUConfigDTO
from dtos.configurations.payments.link import LinkConfigDTO


class PaymentsConfigurationDTO:  # type: ignore[override]
    """
    Aggregated configuration for all supported payment providers.
    """

    stripe: StripeConfigDTO = StripeConfigDTO()
    razorpay: RazorpayConfigDTO = RazorpayConfigDTO()
    paypal: PaypalConfigDTO = PaypalConfigDTO()
    payu: PayUConfigDTO = PayUConfigDTO()
    link: LinkConfigDTO = LinkConfigDTO()


__all__ = [
    "StripeConfigDTO",
    "RazorpayConfigDTO",
    "PaypalConfigDTO",
    "PayUConfigDTO",
    "LinkConfigDTO",
    "PaymentsConfigurationDTO",
]

