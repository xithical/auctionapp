from peewee import (
    AutoField,
    CharField
)

# Models import
from app.classes.models.base_model import BaseModel

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# User Types Model
class User_Types(BaseModel):
    type_id = AutoField(primary_key = True, unique = True)
    type_name = CharField(max_length = 45, unique = True)
    
    class Meta:
        table_name = "User_Types"

# User Types Class/Methods
class UserTypes_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_type(
        type_name: str
    ) -> int:
        """
        Creates a user type in the database

        Args:
            type_name: Name of the user type

        Returns:
            int: The numeric ID of the user type

        Raises:
            PeeweeException: If the type ID already exists
        """
        return User_Types.create(
            type_name=type_name
        ).type_id
    
    @staticmethod
    def get_all_types():
        query = User_Types.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_type_by_id(type_id):
        return User_Types.select().where(User_Types.type_id == type_id).get()
    
    @staticmethod
    def update_type(type_obj):
        return type_obj.save()
    
    @staticmethod
    def delete_type(type_id):
        User_Types.delete().where(User_Types.type_id == type_id).execute()
        return True
    
    @staticmethod
    def get_type_by_name(type_name: str):
        return User_Types.select().where(User_Types.type_name == type_name).get().type_id