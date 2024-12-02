from app.classes.models.merchandise_items import MerchandiseItems_Methods
from app.classes.helpers.merchandise_items_helpers import Merchandise_Item_Helpers
from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.cart_merch_items import CartMerchItems_Methods

class Merchandise_Item_Controller:
    
    @staticmethod
    def list_items():
        output = []
        merch_items = MerchandiseItems_Methods.get_all_items()
        for item in merch_items:
            item_out = Merchandise_Item_Helpers.get_item_details(item["merch_id"])
            output.append(item_out)
        return output
    
    @staticmethod
    def get_merch_item_details(
        item_id
    ):
        return Merchandise_Item_Helpers.get_item_details(item_id)
    
    @staticmethod
    def add_item_to_cart(
        item_id: int,
        user_id: str,
        event_id: int
    ):
        cart_id = MainCart_Methods.get_event_cart_for_user(user_id, event_id)
        return CartMerchItems_Methods.create_entry(cart_id, item_id)