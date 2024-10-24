from peewee import MySQLDatabase

from app.classes.models.base_model import db_proxy

# Import all of our models
from app.classes.models.auction_items import AuctionItems
from app.classes.models.bidder_donations import BidderDonations
from app.classes.models.bids import Bids
from app.classes.models.card_transactions import Card_Transactions
from app.classes.models.cart_auctionitems import Cart_AuctionItems
from app.classes.models.cart_merch_items import CartMerchItems
from app.classes.models.config import Config, Config_Methods
from app.classes.models.events import Events
from app.classes.models.item_donors import ItemDonors
from app.classes.models.main_cart import MainCart
from app.classes.models.merchandise_items import MerchandiseItems
from app.classes.models.user_types import User_Types
from app.classes.models.users import Users

from app.classes.helpers.config_helpers import Config_Helpers

tables = [
    AuctionItems,
    BidderDonations,
    Bids,
    Card_Transactions,
    Cart_AuctionItems,
    CartMerchItems,
    Config,
    Events,
    ItemDonors,
    MainCart,
    MerchandiseItems,
    User_Types,
    Users
]

class Init_Helpers:
    @staticmethod
    def init_db():
        db_config = Config_Helpers.get_db_config()

        database = MySQLDatabase(
            database=db_config["mysql_db"],
            user=db_config["mysql_user"],
            password=db_config["mysql_pass"],
            host=db_config["mysql_host"],
            port=db_config["mysql_port"]
        )

        db_proxy.initialize(database)

        try:
            Config_Helpers.get_latest_config()
            print("Existing installation detected - proceeding with app startup")
        except IndexError:
            print("Fresh installation detected - creating tables now")
            database.create_tables(tables)
            Config_Methods.create_config()

        return database