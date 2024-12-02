from datetime import datetime
from peewee import (
    CharField,
    DateTimeField,
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
    donation_time = DateTimeField()
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
        donation_amount: float,
        user_id: int,
        event_id: int,
        donation_time: datetime = datetime.now()
    ) -> int:
        """
        Creates a donation in the database

        Args:
            donation_amount: Amount of money that is to be donated as a decimal value
        
        Returns:
            int: The numeric ID of the bid

        Raises:
            PeeweeException: If the bid ID already exists or if user_id/event_id fail foreign key constraints
        """
        return BidderDonations.create(
            donation_amount=donation_amount,
            user_id=user_id,
            event_id=event_id,
            donation_time=donation_time
        ).donation_id
    
    @staticmethod
    def get_all_donations():
        query = BidderDonations.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_donations_by_id(donation_id: int):
        return BidderDonations.select().where(BidderDonations.donation_id == donation_id).get()
    
    @staticmethod
    def update_donations(item_obj: object):
        return item_obj.save()
    
    @staticmethod
    def remove_donations(self, donation_id):
        BidderDonations.delete().where(BidderDonations.donation_id == donation_id).execute()
        return True
    
    def get_donations_by_user(user_id: str, event_id: int):
        query = BidderDonations.select().where(BidderDonations.user_id == user_id & BidderDonations.event_id == event_id)
        return DatabaseHelpers.get_rows(query)