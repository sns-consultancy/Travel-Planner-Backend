from typing import Dict

import stripe

from .config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_checkout_session(amount_cents: int, currency: str = "usd", metadata: Dict[str, str] | None = None) -> Dict:
    """Create a Stripe Checkout session."""
    if not stripe.api_key:
        raise RuntimeError("Stripe API key not configured")
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": "Travel Service"},
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        mode="payment",
        metadata=metadata or {},
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return {"sessionId": session.id, "url": session.url}
