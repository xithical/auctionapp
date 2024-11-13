import math
import stripe

from app.classes.helpers.config_helpers import Config_Helpers

class Payments_Helpers:
    @staticmethod
    def create_payment_intent(amount: float):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        amount_cents = math.floor(round(amount, ndigits=2) * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd'
        )

        return intent