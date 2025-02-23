import csv

from io import StringIO

from app.classes.models.auction_items import AuctionItems_Methods
from app.classes.models.users import Users_Methods

from app.classes.helpers.auction_item_helpers import Auction_Items_Helpers

class Reports_Helpers:
    @staticmethod
    def get_auction_report(event_id: int):
        report_lines = []
        output = []
        items = AuctionItems_Methods.get_items_by_event_id(event_id)

        for item in items:
            item_out = {}

            item_details = Auction_Items_Helpers.get_item_details(item["item_id"])
            try:
                winning_bid = Auction_Items_Helpers.get_highest_bid(item["item_id"])
            except:
                winning_bid = None
                print(f"No winning bid for item {item['item_id']} in event {item['event_id']['event_id']}")
            try:
                winning_user = Users_Methods.get_user_by_id(winning_bid["user_id"]["user_id"])
            except:
                winning_user = None
                print(f"No winning user for item {item['item_id']} in event {item['event_id']['event_id']}")

            item_out["event_id"] = item["event_id"]["event_id"]
            item_out["item_id"] = item["item_id"]
            item_out["item_title"] = item["item_title"]
            item_out["item_description"] = item["item_description"]
            item_out["donor_name"] = item_details["donor_name"]
            item_out["item_value"] = item["item_price"]
            if (winning_bid is not None) & (winning_user is not None):
                item_out["winning_bid_amount"] = winning_bid["bid_amount"]
                item_out["winning_bid_time"] = winning_bid["bid_time"]
                item_out["winning_bidder_name"] = f"{winning_user.user_firstname} {winning_user.user_lastname}"
                item_out["winning_bidder_email"] = winning_user.user_email
                item_out["winning_bidder_phone"] = winning_user.user_phone
            else:
                item_out["winning_bid_amount"] = None
                item_out["winning_bid_time"] = None
                item_out["winning_bidder_name"] = None
                item_out["winning_bidder_email"] = None
                item_out["winning_bidder_phone"] = None

            report_lines.append(item_out)

        report_keys = list(report_lines[0].keys())
        output.append(report_keys)

        for line in report_lines:
            line_out = []
            for key in report_keys:
                line_out.append(line[key])
            output.append(line_out)

        csv_out = StringIO()
        csv_writer = csv.writer(csv_out)
        csv_writer.writerows(output)

        return csv_out.getvalue()