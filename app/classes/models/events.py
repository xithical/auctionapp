from peewee import (
    AutoField,
    CharField,
    DateTimeField
)
import datetime

# Models import
from app.classes.models.base_model import BaseModel

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers
from app.classes.helpers.shared_helpers import Helpers

# Events Model
class Events(BaseModel):
    event_id = AutoField(primary_key = True, unique = True)
    event_name = CharField(max_length = 45)
    start_time = DateTimeField()
    end_time = DateTimeField()
    event_code = CharField(max_length = 6, unique = True)

    class Meta:
        table_name = "Events"

# Events Class/Methods
class Events_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_event(
        event_name: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
    ) -> int:
        """
        Creates an auction event in the database

        Args:
            event_name: The displayed name of the event
            start_time: The start time of the event
            end_time: The end time of the event

        Returns:
            int: The numeric event ID

        Raises:
            PeeweeException: If the event ID or event code already exist
        """
        return Events.create(
            event_name=event_name,
            start_time=start_time,
            end_time=end_time,
            event_code=Helpers.create_event_code()
        )
    
    @staticmethod
    def get_all_events():
        query = Events.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_event_by_id(event_id):
        return Events.select().where(Events.event_id == event_id).get()
    
    @staticmethod
    def update_event(event_obj):
        return event_obj.save()
    
    @staticmethod
    def delete_event(event_id):
        Events.delete().where(Events.event_id == event_id).execute()
        return True