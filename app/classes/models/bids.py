from peewee import(
    AutoField,
    CharField,
    ForeignKeyField,
    DateTimeField,
    DecimalField
)
import datetime

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.users import Users
from app.classes.models.auction_items import AuctionItems

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Bids Model
class Bids (BaseModel):
    bid_id= AutoField(primary_key = True, unique=True)
    bid_amount= DecimalField(default =0)
    bid_time = DateTimeField()
    item_id = ForeignKeyField(AuctionItems, to_field="item_id")
    user_id = ForeignKeyField(Users, to_field= "user_id")

    class Meta:
        table_name="Bids"

    #Bids Class/Methods
class Bids_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_bid(
        bid_amount: float,
        bid_time: datetime, 
        item_id: int,
        user_id: int
    ) -> int:
        """
        Creates a bid in the database

        Args:
            bid_amount: The dollar amount the user bids as a decimal
            bid_time: The date and time of the bid
            item_id: The auction item ID; foreign key to Auction_Items table
            user_id: The user ID; foreign key to Users table
           
        Returns:
            int: The numeric ID of the new bid

        Raises:
            PeeweeException: If the bid ID already exists or if user_id or item_id failed foreign key validation
        
        """
        return Bids.create(
            bid_amount=bid_amount,
            bid_time=bid_time,
            item_id=item_id,
            user_id=user_id
        ).bid_id
    
    @staticmethod
    def get_all_bids():
        query = Bids.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_bid_by_id(bid_id: int):
        return Bids.select().where(Bids.bid_id == bid_id)
    
    @staticmethod
    def update_bid(bid_obj: object):
        return bid_obj.save()
    
    @staticmethod
    def remove_bid(bid_id: int):
        Bids.delete().where(Bids.bid_id == bid_id).execute()
        return True
    
    @staticmethod
    def get_bids_by_item_id(item_id: int):
        query = Bids.select().where(Bids.item_id == item_id)
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_bids_by_user_id(user_id: str, event_id: int):
        query = Bids.select().join(AuctionItems).where((Bids.user_id == user_id) & (AuctionItems.event_id == event_id))
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_bids_by_user_and_item(user_id: str, item_id: int):
        query = Bids.select().where(Bids.user_id == user_id & Bids.item_id == item_id)
        return DatabaseHelpers.get_rows(query)