from peewee import(
    AutoField,
    CharField,
    DecimalField,
    ForeignKeyField
)

# Models import
from app.classes.models.base_model import BaseModel
from app.classes.models.users import Users
from app.classes.models.events import Events

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Card Transactions Model
class Card_Transactions(BaseModel):
    transaction_id = AutoField(primary_key = True, unique = True)
    auth_id = CharField(max_length = 45, unique = True)
    amount = DecimalField(decimal_places = 2)
    user_id = ForeignKeyField(Users, to_field = 'user_id')
    event_id = ForeignKeyField(Events, to_field = 'event_id')

    class Meta:
        table_name = 'Card_Transactions'

# Card Transactions Class/Methods
class CardTransactions_Methods:
    def __init__(self, database):
        self.database = database
    
    @staticmethod
    def create_transaction(
        auth_id: str,
        amount: float,
        user_id: int,
        event_id: int
    ) -> int:
        """
        Creates a card transaction in the database

        Args:
            auth_id: The authorization ID from the payment processor
            amount: The decimal amount of the transaction
            user_id: The ID of the user associated with the transaction
            event_id: The ID of the event associated with the transaction

        Returns:
            int: The transaction ID

        Raises:
            PeeweeException: If the transaction ID already exists in the database or if user_id/event_id fail foreign key constraints
        """
        return Card_Transactions.create(
            auth_id=auth_id,
            amount=amount,
            user_id=user_id,
            event_id=event_id
        ).transaction_id
    
    @staticmethod
    def get_all_transactions():
        query = Card_Transactions.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_transaction_by_id(transaction_id: int):
        return Card_Transactions.select().where(Card_Transactions.transaction_id == transaction_id).get()
    
    @staticmethod
    def update_transaction(transaction_obj: object):
        return transaction_obj.save()
    
    @staticmethod
    def delete_transaction(transaction_id: int):
        Card_Transactions.delete().where(Card_Transactions.transaction_id == transaction_id).execute()
        return True