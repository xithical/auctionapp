from app.classes.models.bids import Bids_Methods
from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers

class Bids_Controller():
    def get_user_bids(
      user_id: str,
      event_id: int,      
    ):
        users_bids = Bids_Methods.get_bids_by_user_id(user_id, event_id)
        output = []
        items = []
        for bid in users_bids:
          if bid["item_id"] not in items:
            items.append(bid["item_id"])
        for item in items:
          item_out = {}
          user_bids = Bids_Methods.get_bids_by_user_and_item(user_id, item)
          highest_bid = sorted(user_bids, key=lambda x: x["bid_amount"], reverse=True)[0]
          item = Auction_Items_Helpers.get_item_details(highest_bid["item_id"])
          
          item_out["bid_id"] = highest_bid["bid_id"]
          item_out["item_id"] = item["item_id"]
          item_out["item_title"] = item["item_title"]
          item_out["donor_name"] = item["donor_name"]
          item_out["bid_amount"] = highest_bid["bid_amount"]
          item_out["highest_bid"] = item["highest_bid"]

          output.append[item_out]

        return output