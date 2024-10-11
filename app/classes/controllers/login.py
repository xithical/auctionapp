from datetime import datetime

from app.classes.models.users import Users_Methods
from app.classes.models.events import Events_Methods

from app.classes.helpers.users_helpers import Users_Helpers
from app.classes.helpers.event_helpers import Event_Helpers

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
    def validate_login(email, password):
        try:
            unique_email = Users_Helpers.check_unique_email(email)
            if unique_email:
                user_id = Users_Methods.get_user_by_email(email).user_id
                if Users_Helpers.validate_user_password(user_id):
                    print(f"User {email} successfully logged in")
                    return True
                else:
                    print(f"User {email} tried to login, but entered an invalid password")
                    return False
            else:
                print(f"User {email} tried to login, but does not have a valid account")
                return False
        except Exception as e:
            print(f"Unable to verify user {email}: {e}")
            return False