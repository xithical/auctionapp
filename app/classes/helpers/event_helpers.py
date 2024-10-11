from datetime import datetime

from app.classes.models.events import Events_Methods

class Event_Helpers:
    @staticmethod
    def check_event_code(event_code: str):
        event_code = event_code.upper()
        try:
            event = Events_Methods.get_event_by_code(event_code)
        
        except Exception as e:
            print(f"Unable to retrieve event code {event_code} from the database: {e}")
            return False
        
        if event.end_time > datetime.now():
            return True
        else:
            print(f"Event {event_code} is a valid event, but the end time has passed.")
            return False