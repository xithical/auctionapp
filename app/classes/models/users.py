from peewee import(
    AutoField,
    CharField,
    ForeignKeyField
)

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.user_types import User_Types

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers
from app.classes.helpers.shared_helpers import Helpers

# Users Model
class Users(BaseModel):
    user_id = CharField(max_length = 36, primary_key = True, unique = True)
    user_firstname = CharField(max_length = 45)
    user_lastname = CharField(max_length = 45)
    user_email = CharField(max_length = 255, unique = True)
    user_phone = CharField(max_length = 20)
    user_password = CharField(max_length = 255)
    user_salt = CharField(max_length = 255, unique = True)
    type_id = ForeignKeyField(User_Types, to_field = "type_id")

    class Meta:
        table_name = "Users"

# Users Class/Methods
class Users_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_user(
        user_firstname: str,
        user_lastname: str,
        user_email: str,
        user_phone: str,
        user_password: str,
        type_id: int
    ) -> str:
        """
        Creates a user in the database

        Args:
            user_firstname: The first name of the user
            user_lastname: The last name of the user
            user_email: The email of the user
            user_phone: The phone number of the user
            user_password: The (hashed) password of the user
            type_id: The type of the user; foreign key to User_Types table

        Returns:
            str: The user ID in UUID format

        Raises:
            PeeweeException: If the user ID already exists or if type_id failed foreign key validation
        """
        return Users.create(
            user_id=Helpers.create_uuid(),
            user_firstname=user_firstname,
            user_lastname=user_lastname,
            user_email=user_email,
            user_phone=user_phone,
            user_password=user_password,
            type_id=type_id
        ).user_id
    
    @staticmethod
    def get_all_users():
        query = Users.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_user_by_id(user_id: str):
        return Users.select().where(Users.user_id == user_id).get()
    
    @staticmethod
    def update_user(user_obj: object):
        return user_obj.save()
    
    @staticmethod
    def delete_user(user_id: str):
        Users.delete().where(Users.user_id == user_id).execute()
        return True