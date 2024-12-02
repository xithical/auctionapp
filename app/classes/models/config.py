from peewee import (
    AutoField,
    BooleanField,
    DecimalField,
    CharField,
    IntegerField
)

# Models import
from app.classes.models.base_model import BaseModel

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers
from app.classes.helpers.shared_helpers import Helpers

# Config Model
class Config(BaseModel):
    entry_id = AutoField(primary_key = True, unique = True)
    min_bid_percent = BooleanField()
    min_bid_amount = DecimalField()
    secret_value = CharField(max_length=32)
    entity_name = CharField(max_length=255)
    entity_logo = CharField(max_length=255)
    primary_color = CharField(max_length=7)
    secondary_color = CharField(max_length=7)
    stripe_api_key = CharField(max_length=255)
    tax_id = CharField(max_length=20)
    smtp_user = CharField(max_length=255)
    smtp_email = CharField(max_length=255)
    smtp_server = CharField(max_length=255)
    smtp_port = IntegerField()
    smtp_password = CharField(max_length=255)

    class Meta:
        table_name="Config"

# Config Class/Methods
class Config_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_config(
        min_bid_percent: bool = True,
        min_bid_amount: float = 30,
        secret_value: str = Helpers.generate_secret(),
        entity_name: str = "Silent Auction App",
        entity_logo: str = "/static/assets/img/logo.png",
        primary_color: str = "#21362C", # dark green
        secondary_color: str = "#F6F6F6", # off white
        stripe_api_key: str = "",
        tax_id: str = "",
        smtp_user: str = "",
        smtp_email: str = "",
        smtp_server: str = "",
        smtp_port: int = 0,
        smtp_password: str = ""
    ) -> int:
        """
        Creates a config record in the database

        Args:
            min_bid_percent: If the minimum bid is a percentage; else, it is a fixed value
            min_bid_amount: Minimum bid amount as a whole number; percentage or decimal based on above bool value
            secret_value: Secrets used for encoding/encryption - automatically generated
            entity_name: Name of the entity running the app
            entity_logo: Logo of the entity running the app
            primary_color: The hex color code of the primary UI color
            secondary_color: The hex color code of the secondary UI color
            stripe_api_key: The string of the API key used for Stripe
            tax_id: The Tax ID of the organization
            smtp_user: The SMTP username
            smtp_email: The SMTP email
            smtp_server: The SMTP server
            smtp_port: The SMTP port
            smtp_password: The SMTP password

        Returns:
            int: The numeric ID of the config record

        Raises:
            PeeweeException: If the config ID already exists
        """
        return Config.create(
            min_bid_percent = min_bid_percent,
            min_bid_amount = min_bid_amount,
            secret_value = secret_value,
            entity_name = entity_name,
            entity_logo = entity_logo,
            primary_color = primary_color,
            secondary_color = secondary_color,
            stripe_api_key = stripe_api_key,
            tax_id=tax_id
        ).entry_id
    
    @staticmethod
    def get_all_configs():
        query = Config.select().order_by(Config.entry_id.desc())
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_config_by_id(entry_id):
        return Config.select().where(Config.entry_id == entry_id).get()
    
    @staticmethod
    def update_config(config_obj):
        return config_obj.save()
    
    @staticmethod
    def remove_config(entry_id):
        Config.delete().where(Config.entry_id == entry_id).execute()
        return True