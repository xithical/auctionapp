from datetime import datetime

from app.classes.models.auction_items import AuctionItems_Methods
from app.classes.models.bids import Bids_Methods
from app.classes.models.config import Config_Methods
from app.classes.models.events import Events_Methods
from app.classes.models.item_donors import ItemDonors_Methods
from app.classes.models.merchandise_items import MerchandiseItems_Methods
from app.classes.models.users import Users_Methods

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.reports_helpers import Reports_Helpers
from app.classes.helpers.users_helpers import Users_Helpers

class Admin_Controllers:
    class EventAdmin_Controller:
        @staticmethod
        def list_events():
            events_list = Events_Methods.get_all_events()
            return sorted(events_list, key=lambda x: x["start_time"], reverse=True)
        
        @staticmethod
        def create_event(
            event_name: str,
            start_time: datetime,
            end_time: datetime
        ):
            return Events_Methods.create_event(
                event_name = event_name,
                start_time = start_time,
                end_time = end_time
            )
        
        @staticmethod
        def get_event(event_id: int):
            return Events_Methods.get_event_by_id(event_id)
        
        @staticmethod
        def update_event(
            event_id: int,
            event_name: str,
            start_time: datetime,
            end_time: datetime,
            is_active: bool = True
        ):
            event = Events_Methods.get_event_by_id(event_id)
            event.event_name = event_name
            event.start_time = start_time
            event.end_time = end_time
            event.is_active = is_active
            return Events_Methods.update_event(event)
        
        @staticmethod
        def delete_event(event_id: int):
            return Events_Methods.delete_event(event_id)
        
        @staticmethod
        def list_auction_items(event_id: int):
            return AuctionItems_Methods.get_items_by_event_id(event_id)
        
        @staticmethod
        def get_auction_item(item_id: int):
            return AuctionItems_Methods.get_item_by_id(item_id)
        
        @staticmethod
        def create_auction_item(
            item_title: str,
            item_description: str,
            item_price: float,
            item_image: str,
            donor_id: int,
            event_id: int
        ):
            return AuctionItems_Methods.create_item(
                item_title=item_title,
                item_description=item_description,
                item_price=item_price,
                item_image=item_image,
                donor_id=donor_id,
                event_id=event_id
            )
        
        @staticmethod
        def update_auction_item(
            item_id: int,
            item_title: str,
            item_description: str,
            item_price: float,
            item_image: str,
            donor_id: int,
            event_id: int,
            is_active: bool = True
        ):
            item = AuctionItems_Methods.get_item_by_id(item_id)
            item.item_title = item_title
            item.item_description = item_description
            item.price = item_price
            item.item_image = item_image
            item.donor_id = donor_id
            item.event_id = event_id
            item.is_active = is_active
            return AuctionItems_Methods.update_item(item)
        
        @staticmethod
        def delete_auction_item(item_id: int):
            return AuctionItems_Methods.remove_item(item_id)
        
        @staticmethod
        def get_item_bids(item_id: int):
            bids = Bids_Methods.get_bids_by_item_id(item_id)
            output = []

            for bid in bids:
                bid_out = {}

                bid_out["bid_id"] = bid["bid_id"]
                bid_out["bidder_name"] = f"{bid['user_id']['user_firstname']} {bid['user_id']['user_lastname']}"
                bid_out["bid_time"] = bid["bid_time"]
                bid_out["bid_amount"] = round(bid["bid_amount"], 2)

                output.append(bid_out)
            
            return sorted(output, key = lambda x: x["bid_time"], reverse = True)
        
        @staticmethod
        def delete_bid(bid_id: int):
            return Bids_Methods.remove_bid(bid_id)
        
    class DonorAdmin_Controller:
        @staticmethod
        def list_donors():
            return ItemDonors_Methods.get_all_donors()
        
        @staticmethod
        def get_donor(donor_id: int):
            return ItemDonors_Methods.get_donor_by_id(donor_id)
        
        @staticmethod
        def create_donor(
            donor_firstname: str,
            donor_lastname: str,
            donor_email: str,
            donor_phone: str,
            company_name: str = None
        ):
            donor_email = donor_email.lower()
            return ItemDonors_Methods.create_donor(
                donor_firstname=donor_firstname,
                donor_lastname=donor_lastname,
                donor_email=donor_email,
                donor_phone=donor_phone,
                company_name=company_name
            )
        
        @staticmethod
        def update_donor(
            donor_id: int,
            donor_firstname: str,
            donor_lastname: str,
            donor_email: str,
            donor_phone: str,
            company_name: str = None,
            is_active: bool = True
        ):
            donor_email = donor_email.lower()
            donor = ItemDonors_Methods.get_donor_by_id(donor_id)
            donor.donor_firstname = donor_firstname
            donor.donor_lastname = donor_lastname
            donor.donor_email = donor_email
            donor.donor_phone = donor_phone
            donor.company_name = company_name
            donor.is_active = is_active
            return ItemDonors_Methods.update_donor(donor)
            
        @staticmethod
        def list_donor_items(
            donor_id: int
        ):
            items = AuctionItems_Methods.get_items_by_donor_id(donor_id)
            output = []
            for item in items:
                item_out = {}

                item_out["item_title"] = item["item_title"]
                item_out["event_date"] = item["event_id"]["start_time"]
                item_out["item_price"] = round(item["item_price"], 2)

                output.append(item_out)
            
            return output
        
        @staticmethod
        def delete_donor(donor_id: int):
            return ItemDonors_Methods.remove_donor(donor_id)
    
    class MerchAdmin_Controller:
        @staticmethod
        def list_merch_items():
            return MerchandiseItems_Methods.get_all_items()
        
        @staticmethod
        def get_merch_item(item_id):
            return MerchandiseItems_Methods.get_item_by_id(item_id)
        
        @staticmethod
        def create_merch_item(
            merch_title: str,
            merch_description: str,
            merch_price: float,
            merch_image: str
        ):
            return MerchandiseItems_Methods.create_item(
                merch_title=merch_title,
                merch_description=merch_description,
                merch_price=merch_price,
                merch_image=merch_image
            )
        
        @staticmethod
        def modify_merch_item(
            merch_id: int,
            merch_title,
            merch_description: str,
            merch_price: float,
            merch_image: str,
            is_active: bool = True
        ):
            item = MerchandiseItems_Methods.get_item_by_id(merch_id)
            item.merch_title = merch_title
            item.merch_description = merch_description
            item.merch_price = merch_price
            item.merch_image = merch_image
            item.is_active = is_active
            return MerchandiseItems_Methods.update_item(item)
        
        @staticmethod
        def delete_merch_item(merch_id: int):
            return MerchandiseItems_Methods.remove_item(merch_id)
    
    class UserAdmin_Controller:
        @staticmethod
        def list_users():
            return Users_Methods.get_all_users()
        
        @staticmethod
        def get_user(user_id: str):
            return Users_Methods.get_user_by_id(user_id)
        
        @staticmethod
        def create_user(
            user_firstname: str,
            user_lastname: str,
            user_email: str,
            user_phone: str,
            user_password: str,
            type_id: int
        ):
            hashed_pass = Users_Helpers.hash_password(user_password)
            user_email = user_email.lower()
            return Users_Methods.create_user(
                user_firstname=user_firstname,
                user_lastname=user_lastname,
                user_email=user_email,
                user_phone=user_phone,
                user_password=hashed_pass,
                type_id=type_id
            )
        
        @staticmethod
        def update_user(
            user_id: str,
            user_firstname: str,
            user_lastname: str,
            user_email: str,
            user_phone: str,
            type_id: int,
            user_password: str = None,
            is_active: bool = True
        ):
            user_email = user_email.lower()

            if user_password is not None:
                Users_Helpers.reset_password(
                    user_id=user_id,
                    password=user_password
                )

            user = Users_Methods.get_user_by_id(user_id)
            user.user_firstname = user_firstname
            user.user_lastname = user_lastname
            user.user_email = user_email
            user.user_phone = user_phone
            user.type_id = type_id
            user.is_active = is_active
            
            return Users_Methods.update_user(user)
        
        @staticmethod
        def reset_user_password(
            user_id: str,
            user_password: str
        ):
            return Users_Helpers.reset_password(
                user_id=user_id,
                password=user_password
            )
        
        @staticmethod
        def delete_user(user_id: str):
            return Users_Methods.delete_user(user_id)
    
    class Reports_Controller:
        @staticmethod
        def get_auction_report(event_id: int):
            return Reports_Helpers.get_auction_report(event_id)
        
    class Config_Controller:
        @staticmethod
        def get_config():
            return Config_Helpers.get_latest_config()
        
        @staticmethod
        def update_config(config_obj: object):
            return Config_Methods.update_config(config_obj)