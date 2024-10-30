from app.classes.models.merchandise_items import MerchandiseItems_Methods
from app.classes.helpers.merchandise_items_helpers import Merchandise_Item_Helpers
class Merchandise_Item_Controller():
    
    @staticmethod
    def list_items(
        auction_id: int, 
    ):
        output = []
        merch_items = MerchandiseItems_Methods.get_all_items()
        for item in merch_items:
            item_out = Merchandise_Item_Helpers.get_item_details(item)
            output.append(item_out)
        return output
    
    @staticmethod
    def get_merch_item_details(
        item_id
    ):
        return Merchandise_Item_Helpers.get_item_details(item_id)
    
    