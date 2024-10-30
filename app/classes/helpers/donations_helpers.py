from datetime import datetime

from app.classes.models.bidder_donations import BidderDonation_Methods

class Donations_Helpers:
    @staticmethod
    def place_bid(
        user_id: str,
        event_id: int,
        donation_amount: float,
        donation_time: datetime = datetime.now()
    ):
        return BidderDonation_Methods.create_donation(
            donation_amount=donation_amount,
            user_id=user_id,
            event_id=event_id,
            donation_time=donation_time
        )