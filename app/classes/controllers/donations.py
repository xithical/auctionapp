from datetime import datetime

from app.classes.models.bidder_donations import BidderDonation_Methods

from app.classes.helpers.donations_helpers import Donations_Helpers
from app.classes.helpers.payments_helpers import Payments_Helpers

class Donations_Controller():
    @staticmethod
    def place_donation(
        user_id: str,
        event_id: int,
        donation_amount: float,
        donation_time: datetime = datetime.now()
    ):
        return Payments_Helpers.charge_donation(
            user_id,
            event_id,
            donation_amount
        )
    
    @staticmethod
    def get_donations(
        user_id: str,
        event_id: int
    ):
        return BidderDonation_Methods.get_donations_by_user(
            user_id=user_id,
            event_id=event_id
        )