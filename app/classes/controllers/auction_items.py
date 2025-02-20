from datetime import datetime

from app.classes.models.users import Users_Methods
from app.classes.models.events import Events_Methods

from app.classes.helpers.users_helpers import Users_Helpers
from app.classes.helpers.event_helpers import Event_Helpers
from app.classes.helpers.auth_helpers import Auth_Helpers
from app.classes.models.auction_items import AuctionItems_Methods
from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers
from app.classes.models.item_donors import ItemDonors_Methods
from app.classes.models.bids import Bids_Methods

class Auction_Items_Controller:

    @staticmethod
    def get_items(
        auction_id: int, 
    ):
        return Auction_Items_Helpers.list_items(auction_id)
    
    @staticmethod
    def get_item_details(
        item_id: int
    ):
        return Auction_Items_Helpers.get_item_details(item_id)
    
    @staticmethod
    def place_bid(
        item_id: int,
        user_id: str,
        bid_amount: float,
    ):
        return Auction_Items_Helpers.place_bid(item_id, bid_amount, user_id)