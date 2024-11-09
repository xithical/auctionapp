from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.cart_merch_items import CartMerchItems_Methods
from app.classes.models.cart_auctionitems import Cart_AuctionItems_Methods

from app.classes.helpers.merchandise_items_helpers import Merchandise_Item_Helpers
from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers

class Checkout_Controller:
    @staticmethod
    def list_items(
        user_id: str,
        event_id: int,
        cart_model,
        helper
    ):
        cart = MainCart_Methods.get_event_cart_for_user(user_id, event_id)
        cart_entries = cart_model.get_entries_by_cart(cart)

        output = []
        for entry in cart_entries:
            item = helper.get_item_details(entry["merch_id"])
            output.append(item)

        return output
    
    @staticmethod
    def get_cart(
        user_id: str,
        event_id: int
    ):
        output = {
            "auction_items": [],
            "merch_items": []
        }

        output["auction_items"] = Checkout_Controller.list_items(
            user_id=user_id,
            event_id=event_id,
            cart_model=Cart_AuctionItems_Methods,
            helper=Auction_Items_Helpers
        )
        output["merch_items"] = Checkout_Controller.list_items(
            user_id=user_id,
            event_id=event_id,
            cart_model=CartMerchItems_Methods,
            helper=Merchandise_Item_Helpers
        )

        return output