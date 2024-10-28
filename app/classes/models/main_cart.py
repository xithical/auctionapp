from peewee import (
    AutoField,
    BooleanField,
    ForeignKeyField
)

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.users import Users
from app.classes.models.events import Events

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Auction Items Model
class MainCart(BaseModel):
    cart_id = AutoField(primary_key=True, unique=True)
    user_id = ForeignKeyField(Users, to_field="user_id")
    event_id = ForeignKeyField(Events, to_field="event_id")
    is_active = BooleanField(default = True)
    class Meta:
        table_name = "MainCart"

# MainCart Class/Methods
class MainCart_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_cart(
        user_id: str,
        event_id: int,
        is_active: bool = True
    ) -> int:
        """
        Creates an user cart in the database

        Args:
            user_id: The UUID of the user
            event_id: The numeric ID of the event
        
        Returns:
            int: The numeric ID of the new cart

        Raises:
            PeeweeException: If the cart ID already exists or if user_id/event_id fail foreign key constraints
        """
        return MainCart.create(
            user_id=user_id,
            event_id=event_id,
            is_active=is_active
        ).cart_id
    
    @staticmethod
    def get_all_carts():
        query = MainCart.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_cart_by_id(cart_id: int):
        return MainCart.select().where(MainCart.cart_id == cart_id)
    
    @staticmethod
    def update_cart(item_obj: object):
        return item_obj.save()
    
    def remove_cart(self, cart_id):
        MainCart.delete().where(MainCart.cart_id == cart_id).execute()
        return True