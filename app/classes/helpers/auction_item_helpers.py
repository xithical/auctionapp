from datetime import datetime
from decimal import Decimal
from peewee import fn, JOIN
from playhouse.shortcuts import model_to_dict

from app.classes.models.bids import Bids, Bids_Methods
from app.classes.models.cart_auctionitems import Cart_AuctionItems_Methods
from app.classes.models.main_cart import MainCart_Methods
from app.classes.models.auction_items import AuctionItems, AuctionItems_Methods
from app.classes.models.item_donors import ItemDonors, ItemDonors_Methods

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.db_helpers import DatabaseHelpers

class Auction_Items_Helpers:
    @staticmethod
    def get_starting_bid(
        item_id: int
    ):
        if Config_Helpers.is_min_bid_percent():
            item = AuctionItems_Methods.get_item_by_id(item_id)
            price = item.item_price * (Config_Helpers.get_min_bid_amount()/100)
            return round(price, 2)
        else:
            return round(Config_Helpers.get_min_bid_amount(), 2)

    @staticmethod
    def get_highest_bid(
        item_id: int
    ):
        bids = Bids_Methods.get_bids_by_item_id(item_id)
        sorted_bids = sorted(bids, key=lambda x: x["bid_amount"], reverse=True)
        return sorted_bids[0]

    @staticmethod
    def get_current_bid(
        item_id: int
    ):
        starting_bid = Auction_Items_Helpers.get_starting_bid(item_id)
        try:
            bids = Bids_Methods.get_bids_by_item_id(item_id)
            sorted_bids = sorted(bids, key=lambda x: x["bid_amount"], reverse=True)
            if sorted_bids[0]["bid_amount"] > starting_bid:
                return round(sorted_bids[0]["bid_amount"], 2)
            else:
                return starting_bid
        except Exception as e:
            print(f"{__name__} - Database error: {e}")
            return starting_bid
        
    @staticmethod    
    def get_donor_name(
        donor_id: int
    ):
        donor = ItemDonors_Methods.get_donor_by_id(donor_id)
        
        if donor.company_name is not None:
            donor_name = donor.company_name
        else:
            donor_name = f"{donor.donor_firstname} {donor.donor_lastname}"

        return donor_name
    
    @staticmethod
    def get_item_details(
        item_id: int
    ):
        item_out = {}
        item = AuctionItems_Methods.get_item_by_id(item_id)
        item_out["item_id"] = item.item_id
        item_out["event_id"] = item.event_id.event_id
        item_out["starting_bid"] = Auction_Items_Helpers.get_starting_bid(item.item_id)
        item_out["highest_bid"] = Auction_Items_Helpers.get_current_bid(item.item_id)
        item_out["price"] = Auction_Items_Helpers.get_current_bid(item.item_id)
        item_out["donor_name"] = Auction_Items_Helpers.get_donor_name(item.donor_id)
        item_out["item_image"] = item.item_image
        item_out["item_title"] = item.item_title
        item_out["item_description"] = item.item_description
        item_out["num_bids"] = len(Bids_Methods.get_bids_by_item_id(item_id))
        return item_out
    
    @staticmethod
    def place_bid(
        item_id: int,
        amount: float,
        user_id: str
    ):
        bid = round(float(amount), ndigits=2)
        highest_bid = Auction_Items_Helpers.get_current_bid(item_id)
        item = AuctionItems_Methods.get_item_by_id(item_id)
        event_id = item.event_id.event_id
        if bid > highest_bid:
            Cart_AuctionItems_Methods.remove_entries_for_item(item_id)
            bid = Bids_Methods.create_bid(
                item_id=item_id,
                bid_amount=bid,
                user_id=user_id,
                bid_time=datetime.now()
            )
            Cart_AuctionItems_Methods.create_entry(
                cart_id=MainCart_Methods.get_event_cart_for_user(user_id, event_id),
                bid_id=bid
            )
            return bid
        else:
            return None
        
    @staticmethod
    def get_item_id(item: dict):
        return item["bid_id"]["item_id"]["item_id"]
    
    @staticmethod
    def list_items(event_id: int):
        min_bid_percent = Config_Helpers.is_min_bid_percent()
        min_bid_amount = Config_Helpers.get_min_bid_amount()/100

        if min_bid_percent:
            query = (
                AuctionItems
                .select(
                    AuctionItems.item_id,
                    AuctionItems.event_id,
                    fn.ROUND(AuctionItems.item_price, 2).alias("item_price"),
                    fn.ROUND((AuctionItems.item_price * min_bid_amount), 2).alias("starting_bid"),
                    fn.ROUND(fn.COALESCE(fn.MAX(Bids.bid_amount), (AuctionItems.item_price * min_bid_amount)), 2).alias("highest_bid"),
                    fn.COUNT(Bids.bid_id).alias("num_bids"),
                    fn.COALESCE(ItemDonors.company_name, fn.CONCAT(ItemDonors.donor_firstname, ' ', ItemDonors.donor_lastname)).alias("donor_name"),
                    AuctionItems.item_image,
                    AuctionItems.item_title,
                    AuctionItems.item_description
                )
                .join(ItemDonors, JOIN.LEFT_OUTER, on=(AuctionItems.donor_id == ItemDonors.donor_id))
                .join(Bids, JOIN.LEFT_OUTER, on=(AuctionItems.item_id == Bids.item_id))
                .where(AuctionItems.event_id == event_id)
                .group_by(AuctionItems.item_id)
            )
        else:
            query = (
                AuctionItems
                .select(
                    AuctionItems.item_id,
                    AuctionItems.event_id,
                    fn.ROUND(AuctionItems.item_price, 2).alias("item_price"),
                    fn.ROUND(min_bid_amount, 2).alias("starting_bid"),
                    fn.ROUND(fn.COALESCE(fn.MAX(Bids.bid_amount), (min_bid_amount)), 2).alias("highest_bid"),
                    fn.COUNT(Bids.bid_id).alias("num_bids"),
                    fn.COALESCE(ItemDonors.company_name, fn.CONCAT(ItemDonors.donor_firstname, ' ', ItemDonors.donor_lastname)).alias("donor_name"),
                    AuctionItems.item_image,
                    AuctionItems.item_title,
                    AuctionItems.item_description
                )
                .join(ItemDonors, JOIN.LEFT_OUTER, on=(AuctionItems.donor_id == ItemDonors.donor_id))
                .join(Bids, JOIN.LEFT_OUTER, on=(AuctionItems.item_id == Bids.item_id))
                .where(AuctionItems.event_id == event_id)
                .group_by(AuctionItems.item_id)
            )

        return query.dicts()