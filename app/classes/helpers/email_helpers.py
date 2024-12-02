import os
import smtplib

from decimal import Decimal
from jinja2 import Environment, FileSystemLoader

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.classes.models.bidder_donations import BidderDonation_Methods
from app.classes.models.events import Events_Methods
from app.classes.models.item_donors import ItemDonors_Methods
from app.classes.models.users import Users_Methods

from app.classes.controllers.checkout import Checkout_Controller

from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers
from app.classes.helpers.config_helpers import Config_Helpers

environment = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'receipt_templates')))

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
        
        @staticmethod
        def donation_receipt(donation_id: int):
            donation = BidderDonation_Methods.get_donations_by_id(donation_id)
            user = donation.user_id
            event = donation.event_id

            template = environment.get_template("donation.html")

            amount = round(donation.donation_amount, ndigits=2)

            return template.render(
                org_name=Config_Helpers.get_entity_name(),
                name=f"{user.user_firstname} {user.user_lastname}",
                event_name=event.event_name,
                start_time=event.start_time,
                donation_time=donation.donation_time,
                amount=amount
            )
        
        @staticmethod
        def item_donor_receipt(donor_id: int, event_id, items: list, total: Decimal):
            donor_name = Auction_Items_Helpers.get_donor_name(donor_id)
            event = Events_Methods.get_event_by_id(event_id)

            template = environment.get_template("item_donor.html")

            return template.render(
                org_name=Config_Helpers.get_entity_name(),
                name=donor_name,
                event_name=event.event_name,
                end_time=event.end_time,
                total=total,
                items=items
            )
    
    class Senders:
        @staticmethod
        def event_receipt(user_id: str, event_id: int):
            user = Users_Methods.get_user_by_id(user_id)
            event = Events_Methods.get_event_by_id(event_id)
            org_name = Config_Helpers.get_entity_name()

            sender = Config_Helpers.get_smtp_email()
            recipient = user.user_email
            smtp_user = Config_Helpers.get_smtp_user()
            smtp_pass = Config_Helpers.get_smtp_password()
            smtp_server = Config_Helpers.get_smtp_server()
            smtp_port = Config_Helpers.get_smtp_port()

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{org_name}: Event Receipt for {event.event_name} on {event.end_time}"
            msg['From'] = sender
            msg['To'] = recipient

            text = f"Event receipt for {event.event_name} on {event.end_time}. To view this receipt, please open in a modern mail client that supports HTML messages."
            html = Email_Helpers.Templates.event_receipt(user_id, event_id)

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            mail = smtplib.SMTP(smtp_server, smtp_port)

            mail.ehlo()
            mail.starttls()

            mail.login(smtp_user, smtp_pass)
            mail.sendmail(sender, recipient, msg.as_string())
            mail.quit()

            return True
        
        @staticmethod
        def donation_receipt(user_id: str, event_id: int, donation_id: int):
            user = Users_Methods.get_user_by_id(user_id)
            event = Events_Methods.get_event_by_id(event_id)
            donation = BidderDonation_Methods.get_donations_by_id(donation_id)
            org_name = Config_Helpers.get_entity_name()

            sender = Config_Helpers.get_smtp_email()
            recipient = user.user_email
            smtp_user = Config_Helpers.get_smtp_user()
            smtp_pass = Config_Helpers.get_smtp_password()
            smtp_server = Config_Helpers.get_smtp_server()
            smtp_port = Config_Helpers.get_smtp_port()

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{org_name}: Donation Receipt for {event.event_name} on {donation.donation_time}"
            msg['From'] = sender
            msg['To'] = recipient

            text = f"Donation receipt for {event.event_name} on {donation.donation_time}. To view this receipt, please open in a modern mail client that supports HTML messages."
            html = Email_Helpers.Templates.donation_receipt(donation_id)

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            mail = smtplib.SMTP(smtp_server, smtp_port)

            mail.ehlo()
            mail.starttls()

            mail.login(smtp_user, smtp_pass)
            mail.sendmail(sender, recipient, msg.as_string())
            mail.quit()

            return True
        
        @staticmethod
        def item_donor_receipt(donor_id: int, event_id: int, items: list, total: Decimal):
            donor = ItemDonors_Methods.get_donor_by_id(donor_id)
            event = Events_Methods.get_event_by_id(event_id)
            org_name = Config_Helpers.get_entity_name()

            sender = Config_Helpers.get_smtp_email()
            recipient = donor.donor_email
            smtp_user = Config_Helpers.get_smtp_user()
            smtp_pass = Config_Helpers.get_smtp_password()
            smtp_server = Config_Helpers.get_smtp_server()
            smtp_port = Config_Helpers.get_smtp_port()

            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"{org_name}: Donation Receipt for {event.event_name} on {event.end_time}"
            msg['From'] = sender
            msg['To'] = recipient

            text = f"Donation receipt for {event.event_name} on {event.end_time}. To view this receipt, please open in a modern mail client that supports HTML messages."
            html = Email_Helpers.Templates.item_donor_receipt(
                donor_id,
                event_id,
                items,
                total
            )

            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            msg.attach(part1)
            msg.attach(part2)

            mail = smtplib.SMTP(smtp_server, smtp_port)

            mail.ehlo()
            mail.starttls()

            mail.login(smtp_user, smtp_pass)
            mail.sendmail(sender, recipient, msg.as_string())
            mail.quit()

            return True