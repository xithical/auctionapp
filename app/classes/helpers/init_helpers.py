from peewee import MySQLDatabase, DoesNotExist

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
from app.classes.models.user_types import User_Types, UserTypes_Methods
from app.classes.models.users import Users, Users_Methods

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.shared_helpers import Helpers
from app.classes.helpers.users_helpers import Users_Helpers

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
    def init_roles():
        # Admin Role
        try:
            UserTypes_Methods.get_type_by_name("Admin")
        except:
            print("Unable to retrieve Admin user type from database - creating.")
            UserTypes_Methods.create_type(type_name = "Admin")

        # User Role
        try:
            UserTypes_Methods.get_type_by_name("User")
        except:
            print("Unable to retrieve User user type from database - creating.")
            UserTypes_Methods.create_type(type_name = "User")

        return UserTypes_Methods.get_all_types()
    
    @staticmethod
    def init_admin():
        admin_role = UserTypes_Methods.get_type_by_name("Admin")
        admins = Users_Methods.get_all_users_for_type(admin_role.type_id)

        if len(admins) == 0:
            temp_pass = Helpers.generate_secret()
            new_admin = Users_Methods.create_user(
                user_firstname="Admin",
                user_lastname="User",
                user_email="admin@example.com",
                user_phone="5555555555",
                user_password=Users_Helpers.hash_password(temp_pass),
                type_id=admin_role.type_id,
                is_active=True
            )
            
            with open("app/config/default_creds.txt", "w") as f:
                f.write(f"admin@example.com\n{temp_pass}")
            
            return new_admin
        else:
            return admins[0]["user_id"]
    
    @staticmethod
    def init_db(scheduler: bool = False):
        db_config = Config_Helpers.get_db_config()

        database = MySQLDatabase(
            database=db_config["mysql_db"],
            user=db_config["mysql_user"],
            password=db_config["mysql_pass"],
            host=db_config["mysql_host"],
            port=db_config["mysql_port"]
        )

        db_proxy.initialize(database)

        if not scheduler:
            try:
                Config_Helpers.get_latest_config()
                print("Existing installation detected - proceeding with app startup")
            except IndexError:
                print("Fresh installation detected - creating tables now")
                database.create_tables(tables)
                Config_Methods.create_config()
            
            Init_Helpers.init_roles()
            Init_Helpers.init_admin()

        return database