from peewee import (
    CharField,
    DecimalField,
    AutoField,
)

# Models import
from app.classes.models.base_model import BaseModel

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Merchandise Items Model
class AuctionItems(BaseModel):
    item_id = AutoField(primary_key=True, unique=True)
    item_title = CharField(default="", max_length = 100)
    item_description = CharField(default = "", max_length = 255)
    item_price = DecimalField(default = 0)
    item_image = CharField(default = "", max_length = 1000)
    donor_id = AutoField(primary_key=False,)
    event_id = AutoField(primary_key=False,)
    class Meta:
        table_name = "AuctionItems"

# Merchandise Items Class/Methods
class MerchandiseItems_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_item(
        item_title: str,
        item_description: str,
        item_price: float,
        item_image: str
    ) -> int:
        """
        Creates an auction item in the database

        Args:
            auction_item_title: The name/title of the merch item
            auction_item_description: A brief description of the item
            auction_item_price: The price (in dollars) of the item
            auction_item_image: The path to the item image
        
        Returns:
            int: The numeric ID of the new item

        Raises:
            PeeweeException: If the item ID already exists
        """
        return AuctionItems.create(
            auction_item_title=item_title,
            auction_item_description=item_description,
            auction_item_price=item_price,
            auction_item_image=item_image
        ).auction_item_id
    
    @staticmethod
    def get_all_items():
        query = AuctionItems.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_item_by_id(item_id: int):
        return AuctionItems.select().where(AuctionItems.auction_item_id == item_id)
    
    @staticmethod
    def update_item(item_obj: object):
        return item_obj.save()
    
    def remove_item(self, item_id):
        AuctionItems.delete().where(AuctionItems.auction_item_id == item_id).execute()
        return True