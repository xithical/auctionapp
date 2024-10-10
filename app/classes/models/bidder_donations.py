from peewee import (
    CharField,
    DecimalField,
    AutoField,
    ForeignKeyField
)

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.users import Users
from app.classes.models.events import Events

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Auction Items Model
class BidderDonations(BaseModel):
    donation_id = AutoField(primary_key=True, unique=True)
    donation_amount = DecimalField(default = 0)
    user_id = ForeignKeyField(Users, to_field="user_id")
    event_id = ForeignKeyField(Events, to_field="event_id")
    class Meta:
        table_name = "BidderDonations"

# Auction Items Class/Methods
class BidderDonation_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_donation(
        donation_id: int,
        donation_amount: float,
        user_id: int,
        event_id: int
    ) -> int:
        """
        Creates a donation item in the database

        Args:
        donation_amount: amount of money that is to be donated
        
        Returns:
            int: The numeric ID of the new item

        Raises:
            PeeweeException: If the item ID already exists
        """
        return BidderDonations.create(
            donation_id=donation_id,
            donation_amount=donation_amount,
            user_id=user_id,
            event_id=event_id
        ).donation_id
    
    @staticmethod
    def get_all_donations():
        query = BidderDonations.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_donations_by_id(donation_id: int):
        return BidderDonations.select().where(BidderDonations.donation_id_id == donation_id)
    
    @staticmethod
    def update_donations(item_obj: object):
        return item_obj.save()
    
    def remove_donations(self, donation_id):
        BidderDonations.delete().where(BidderDonations.donation_id == donation_id).execute()
        return True