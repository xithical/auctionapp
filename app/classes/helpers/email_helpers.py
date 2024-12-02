import smtplib

from jinja2 import Environment, FileSystemLoader

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.classes.models.events import Events_Methods
from app.classes.models.users import Users_Methods

from app.classes.controllers.checkout import Checkout_Controller

from app.classes.helpers.config_helpers import Config_Helpers

environment = Environment(loader=FileSystemLoader("receipt_templates/"))

class Email_Helpers:
    class Templates:
        @staticmethod
        def event_receipt(user_id: str, event_id: int):
            cart = Checkout_Controller.get_cart(user_id, event_id)
            user = Users_Methods.get_user_by_id(user_id)
            event = Events_Methods.get_event_by_id(event_id)

            template = environment.get_template("event.html")

            total = cart["auction_items"]["price_total"] + cart["merch_items"]["price_total"]

            return template.render(
                org_name=Config_Helpers.get_entity_name(),
                name=f"{user.user_firstname} {user.user_lastname}",
                event_name=event.event_name,
                end_time=event.end_time,
                auction_items=cart["auction_items"]["items"],
                merch_items=cart["merch_items"]["items"],
                auction_total=cart["auction_items"]["price_total"],
                merch_total=cart["merch_items"]["price_total"],
                total=total
            )