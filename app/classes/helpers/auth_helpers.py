import jwt
from datetime import datetime, timedelta

from app.classes.helpers.users_helpers import Users_Helpers
from app.classes.helpers.event_helpers import Event_Helpers
from app.classes.helpers.config_helpers import Config_Helpers

from app.classes.models.auction_items import AuctionItems_Methods
from app.classes.models.users import Users_Methods

class Auth_Helpers:
    @staticmethod
    def validate_login(email, password):
        try:
            unique_email = Users_Helpers.check_unique_email(email)
            if not unique_email:
                user = Users_Methods.get_user_by_email(email)
                if Users_Helpers.validate_user_password(user.user_id, password):
                    print(f"User {email} successfully logged in")
                    return user
                else:
                    print(f"User {email} tried to login, but entered an invalid password")
                    return None
            else:
                print(f"User {email} tried to login, but does not have a valid account")
                return None
        except Exception as e:
            print(f"Unable to verify user {email}: {e}")
            return None
        
    @staticmethod
    def validate_session(current_user, session, item_id: int = None):
        if "event_id" not in session:
            return "event_id"
        if Event_Helpers.validate_event(session["event_id"]):
            if item_id is not None:
                item = AuctionItems_Methods.get_item_by_id(item_id)
                if item.event_id.event_id == int(session["event_id"]):
                    return True
                else:
                    return "item_id"
            else:
                return True
        else:
            return "event_id"