import json
from peewee import MySQLDatabase

from app.classes.models.base_model import db_proxy

# Import all of our models
from app.classes.models.auction_items import AuctionItems
from app.classes.models.bidder_donations import BidderDonations
from app.classes.models.bids import Bids
from app.classes.models.card_transactions import Card_Transactions
from app.classes.models.cart_auctionitems import Cart_AuctionItems
from app.classes.models.cart_merch_items import CartMerchItems
from app.classes.models.config import Config
from app.classes.models.events import Events
from app.classes.models.item_donors import ItemDonors
from app.classes.models.main_cart import MainCart
from app.classes.models.merchandise_items import MerchandiseItems
from app.classes.models.user_types import User_Types
from app.classes.models.users import Users

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

def get_db_config():
    with open('app/config/db_settings.json', 'r') as db_config:
        data = json.load(db_config)
    return data

if __name__ == "__main__":
    db_config = get_db_config()
    database = MySQLDatabase(
        database=db_config["mysql_db"],
        user=db_config["mysql_user"],
        password=["mysql_pass"],
        host=db_config["mysql_host"],
        port=db_config["mysql_port"]
    )
    database.connect()
    db_proxy.initialize(database)

    database.create_tables(tables)

    exit()