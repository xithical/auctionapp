import math
import stripe

from app.classes.models.users import Users_Methods

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
    
    @staticmethod
    def verify_customer(user_id):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        user = Users_Methods.get_user_by_id(user_id)
        customers = stripe.Customer.search(query=f"email~'{user.user_email}'")
        if len(customers) == 0:
            customer = stripe.Customer.create(
                name=f"{user.user_firstname} {user.user_lastname}",
                email=user.user_email
            )
        else:
            customer = customers.data[0]
        return customer["id"]
    
    @staticmethod
    def create_checkout_session(customer_id: str, success_url: str):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        return stripe.checkout.Session.create(
            mode="setup",
            currency="usd",
            customer=customer_id,
            success_url=success_url,
            payment_method_types=["card"]
        )