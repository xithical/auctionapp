from datetime import datetime

from app.classes.models.users import Users_Methods
from app.classes.models.user_types import UserTypes_Methods
from app.classes.models.events import Events_Methods

from app.classes.helpers.users_helpers import Users_Helpers
from app.classes.helpers.event_helpers import Event_Helpers
from app.classes.helpers.auth_helpers import Auth_Helpers

class User_Registration_Controller():
    @staticmethod
    def register_user(
        user_firstname: str,
        user_lastname: str,
        user_email: str,
        user_phone: str,
        user_password: str,
        event_code: str,
        type_id: int = None
    ):
        user_email = user_email.lower()
        event_code = event_code.upper()
        user_password = Users_Helpers.hash_password(user_password)
        if type_id is None:
            type_id = UserTypes_Methods.get_type_by_name("User").type_id

        email_valid = Users_Helpers.check_unique_email(user_email)
        event_valid = Event_Helpers.check_event_code(event_code)
        type_valid = Users_Helpers.check_valid_user_type(type_id)

        if email_valid & event_valid & type_valid:
            return Users_Methods.create_user(
                user_firstname=user_firstname,
                user_lastname=user_lastname,
                user_email=user_email,
                user_phone=user_phone,
                user_password=user_password,
                type_id=type_id
            )
        elif not email_valid:
            print(f"{__name__} - User {user_email} tried to register, but the email address is already in use")
            return False
        elif not event_valid:
            print(f"{__name__} - User {user_email} tried to register, but the event code {event_code} is invalid")
            return False
        elif not type_valid:
            print(f"{__name__} - User {user_email} tried to register, but the type ID {type_id} is invalid")
            return False
        else:
            print(f"{__name__} - User {user_email} tried to register, but the process encountered an unknown error")
            return False

class User_Login_Controller:
    @staticmethod
    def login_user(email: str, password: str, event_code: str):
        email = email.lower()
        event_code = event_code.upper()

        valid_auth = Auth_Helpers.validate_login(email, password)
        valid_event = Event_Helpers.check_event_code(event_code)

        if (valid_auth is not None) & valid_event:
            return valid_auth
        elif valid_auth is None:
            return None
        elif not valid_event:
            return None
        
    @staticmethod
    def login_admin(email: str, password: str):
        email = email.lower()

        valid_auth = Auth_Helpers.validate_login(email, password)
        admin_user = Users_Helpers.is_user_admin(user_id = valid_auth.user_id)

        if (valid_auth is not None) & admin_user:
            return valid_auth
        elif valid_auth is None:
            return None
        elif not admin_user:
            print(f"User {email} tried to log into the admin page, but they do not have permission.")
            return None
    
    @staticmethod
    def get_user(user_id: str):
        try:
            return Users_Methods.get_user_by_id(user_id)
        except:
            return None
        
    @staticmethod
    def is_admin(user_id: str):
        return Users_Helpers.is_user_admin(user_id)