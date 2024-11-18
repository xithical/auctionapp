import jwt
from datetime import datetime, timedelta

from app.classes.helpers.users_helpers import Users_Helpers
from app.classes.helpers.event_helpers import Event_Helpers
from app.classes.helpers.config_helpers import Config_Helpers
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
    def issue_jwt_user(user_id: str, event_id: int):
        expiration = datetime.now() + timedelta(hours=24)
        encoded_jwt = jwt.encode(
            {
                "user_id": user_id,
                "event_id": event_id,
                "valid_to": expiration
            },
            Config_Helpers.get_secret_value(),
            algorithm="HS256"
        )
        return encoded_jwt
    
    @staticmethod
    def issue_jwt_admin(user_id: str):
        expiration = datetime.now() + timedelta(hours=24)
        encoded_jwt = jwt.encode(
            {
                "user_id": user_id,
                "valid_to": expiration
            },
            Config_Helpers.get_secret_value(),
            algorithm="HS256"
        )
        return encoded_jwt