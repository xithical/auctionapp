import math
import stripe

from decimal import Decimal

from app.classes.models.card_transactions import CardTransactions_Methods
from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.users import Users_Methods

from app.classes.controllers.checkout import Checkout_Controller

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.donations_helpers import Donations_Helpers

class Payments_Helpers:
    @staticmethod
    def create_payment_intent(
        amount: Decimal,
        customer_id: str,
        payment_method: str
    ):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        amount_cents = math.floor(round(amount, ndigits=2) * 100)

        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency='usd',
            customer=customer_id,
            payment_method=payment_method,
            confirm=True,
            off_session=True
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
    
    @staticmethod
    def verify_checkout_session(checkout_session: str):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        try:
            stripe.checkout.Session.retrieve(checkout_session)
            return True
        except Exception as e:
            print(f"{__name__} - Unable to retrieve Stripe checkout session {checkout_session}: {e}")
            return False
        
    @staticmethod
    def charge_donation(user_id: str, event_id: int, amount: Decimal):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        cart = MainCart_Methods.get_event_cart_for_user(
            user_id=user_id,
            event_id=event_id
        )
        checkout_session_id = MainCart_Methods.get_cart_by_id(cart).checkout_session
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        setup_intent = stripe.SetupIntent.retrieve(checkout_session["setup_intent"])
        payment_method = setup_intent["payment_method"]
        payment_intent = Payments_Helpers.create_payment_intent(
            amount = amount,
            customer_id=setup_intent["customer"],
            payment_method=payment_method
        )
        if payment_intent["status"] == "succeeded":
            print(f"{__name__} - Payment succeeded for user {user_id}, amount ${amount}")
            donation = Donations_Helpers.place_donation(
                user_id=user_id,
                event_id=event_id,
                donation_amount=amount
            )
            transaction = CardTransactions_Methods.create_transaction(
                auth_id = payment_intent["latest_charge"],
                amount = amount,
                user_id = user_id,
                event_id = event_id
            )
            return {
                "donation": donation,
                "transaction": transaction
            }
        else:
            print(f"{__name__} - Payment failed for user {user_id}, amount ${amount}")
            return None
    
    @staticmethod
    def charge_cart(cart_id: int):
        stripe.api_key = Config_Helpers.get_stripe_api_key()
        cart = MainCart_Methods.get_cart_by_id(cart_id)
        user_id = cart.user_id.user_id
        event_id = cart.event_id.event_id
        cart_summary = Checkout_Controller.get_cart(user_id, event_id)

        amount = cart_summary["auction_items"]["price_total"] + cart_summary["merch_items"]["price_total"]
        
        checkout_session_id = MainCart_Methods.get_cart_by_id(cart).checkout_session
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        setup_intent = stripe.SetupIntent.retrieve(checkout_session["setup_intent"])
        payment_method = setup_intent["payment_method"]
        payment_intent = Payments_Helpers.create_payment_intent(
            amount = amount,
            customer_id=setup_intent["customer"],
            payment_method=payment_method
        )
        if payment_intent["status"] == "succeeded":
            print(f"{__name__} - Payment succeeded for user {user_id}, amount ${amount}")
            transaction = CardTransactions_Methods.create_transaction(
                auth_id = payment_intent["latest_charge"],
                amount = amount,
                user_id = user_id,
                event_id = event_id
            )
            return transaction
        else:
            print(f"{__name__} - Payment failed for user {user_id}, amount ${amount}")
            return None