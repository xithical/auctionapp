from datetime import datetime

from app.classes.models.users import Users_Methods
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
        type_id: int,
        event_code: str
    ):
        user_email = user_email.lower()
        event_code = event_code.upper()
        user_password = Users_Helpers.hash_password(user_password)

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
            return "Email address is already in use"
        elif not event_valid:
            return "Invalid event ID"
        elif not type_valid:
            return "Invalid user type"
        else:
            return "Unknown error"

class User_Login_Controller:
    @staticmethod
    def login_user(email: str, password: str, event_code: str):
        email = email.lower()
        event_code = event_code.upper()

        valid_auth = Auth_Helpers.validate_login(email, password)
        valid_event = Event_Helpers.check_event_code(event_code)

        if valid_auth & valid_event:
            user_id = Users_Methods.get_user_by_email(email)
            event_id = Events_Methods.get_event_by_code(event_code)
            return Auth_Helpers.issue_jwt_user(user_id, event_id)
        elif not valid_auth:
            return None
        elif not valid_event:
            return None
        
    @staticmethod
    def login_admin(email: str, password: str):
        email = email.lower()

        valid_auth = Auth_Helpers.validate_login(email, password)
        admin_user = Users_Helpers.is_user_admin(user_email = email)

        if valid_auth & admin_user:
            user_id = Users_Methods.get_user_by_email(email)
            return Auth_Helpers.issue_jwt_admin(user_id)
        elif not valid_auth:
            return None
        elif not admin_user:
            print(f"User {email} tried to log into the admin page, but they do not have permission.")
            return None