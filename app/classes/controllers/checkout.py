from datetime import datetime
from decimal import Decimal

from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.cart_merch_items import CartMerchItems_Methods
from app.classes.models.cart_auctionitems import Cart_AuctionItems_Methods
from app.classes.models.users import Users_Methods

from app.classes.helpers.merchandise_items_helpers import Merchandise_Item_Helpers
from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers
from app.classes.helpers.donations_helpers import Donations_Helpers

class Checkout_Controller:
    @staticmethod
    def list_items(
        cart,
        cart_model,
        helper
    ):
        cart_entries = cart_model.get_entries_by_cart(cart)

        cart_value = Decimal(0.00)
        output = {
            "items": []
        }
        for entry in cart_entries:
            item_id = helper.get_item_id(entry)
            item = helper.get_item_details(item_id)
            item_out = {
                "key": entry["entry_id"],
                "value": item
            }
            output["items"].append(item_out)
            cart_value += item["price"]
        output["price_total"] = cart_value
        return output
    
    @staticmethod
    def get_cart(
        user_id: str,
        event_id: int
    ):
        cart = MainCart_Methods.get_event_cart_for_user(user_id, event_id)
        output = {
            "cart_id": cart,
            "auction_items": [],
            "merch_items": []
        }

        output["auction_items"] = Checkout_Controller.list_items(
            cart_model=Cart_AuctionItems_Methods,
            helper=Auction_Items_Helpers,
            cart=cart
        )
        output["merch_items"] = Checkout_Controller.list_items(
            cart_model=CartMerchItems_Methods,
            helper=Merchandise_Item_Helpers,
            cart=cart
        )

        return output
    
    @staticmethod
    def place_donation(
        user_id: str,
        event_id: int,
        donation_amount: float,
        donation_time: datetime = datetime.now()
    ):
        return Donations_Helpers.place_donation(
            user_id=user_id,
            event_id=event_id,
            donation_amount=donation_amount,
            donation_time=donation_time
        )
    
    @staticmethod
    def get_user(user_id: str):
        return Users_Methods.get_user_by_id(user_id)
    
    @staticmethod
    def create_cart(user_id: str, event_id: int, checkout_session: str):
        return MainCart_Methods.create_cart(
            user_id=user_id,
            event_id=event_id,
            checkout_session=checkout_session
        )
    
    @staticmethod
    def remove_merchcart_entry(cart_id: int, entry_id: int):
        entry = CartMerchItems_Methods.get_entry_by_id(entry_id)
        if entry.cart_id.cart_id == cart_id:
            return CartMerchItems_Methods.remove_entry(entry_id)
        else:
            return None