from peewee import (
    CharField,
    AutoField,
    ForeignKeyField
)

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.main_cart import MainCart ## Waiting for main cart
from app.classes.models.bids import Bids

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Cart Auction Items Model
class Cart_AuctionItems (BaseModel):
    entry_id= AutoField(primary_key = True, unique=True)
    cart_id= ForeignKeyField(MainCart, to_field ="cart_id") #Come back and check cart table
    bid_id = ForeignKeyField(Bids, to_field = "bid_id")

    class Meta:
        table_name="Cart_AuctionItems"

#Cart_AuctionItems Class/Methods
class Cart_AuctionItems_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_entry(
        cart_id: int, 
        bid_id: int,
    ) -> int:
        """
         Creates a Cart specifically for Auction Items in the database

        Args:
            cart_id: The main cart ID; foreign key to the Cart table
            bid_id: The bid ID; foreign key to Bids table
           
        Returns:
            int: The numeric ID of the new entry into the auction item cart

        Raises:
            PeeweeException: If the entry ID already exists or if cart_id or bid_id failed foreign key validation
        
        """
        return Cart_AuctionItems.create(
            cart_id=cart_id,
            bid_id=bid_id
        ).entry_id
    
    @staticmethod
    def get_all_entries():
        query = Cart_AuctionItems.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_entry_by_id(entry_id: int):
        return Cart_AuctionItems.select().where(Cart_AuctionItems.entry_id == entry_id)
    
    @staticmethod
    def update_entry(entry_obj: object):
        return entry_obj.save()
    
    def remove_entry(self, entry_id):
        Cart_AuctionItems.delete().where(Cart_AuctionItems.entry_id == entry_id).execute()
        return True