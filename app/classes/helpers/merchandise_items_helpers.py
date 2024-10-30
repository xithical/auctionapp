from app.classes.models.merchandise_items import MerchandiseItems_Methods
from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.cart_merch_items import CartMerchItems_Methods

class Merchandise_Item_Helpers():
    
    @staticmethod
    def get_item_details(
        item_id: int
    ):
        item_out = {}
        item = MerchandiseItems_Methods.get_item_by_id(item_id)
        item_out["item_id"] = item["item_id"]
        item_out["item_image"] = item["item_image"]
        item_out["item_title"] = item["item_title"]
        item_out["price"] = item["price"]
        return item_out
        
    @staticmethod
    def get_items():
        return MerchandiseItems_Methods.get_all_items()
    
    @staticmethod
    def add_item_to_cart(
        user_id: str,
        item_id: int,
        event_id: int
    ):
        cart_id = MainCart_Methods.get_event_cart_for_user(user_id=user_id, event_id=event_id)
        
        if cart_id is None:
            cart_id = MainCart_Methods.create_cart(user_id, event_id)

        return CartMerchItems_Methods.create_entry(cart_id, item_id)