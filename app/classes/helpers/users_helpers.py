from argon2 import (
    PasswordHasher,
    exceptions as ArgonExceptions
)

from app.classes.models.users import Users_Methods
from app.classes.models.user_types import UserTypes_Methods

password_hasher = PasswordHasher()

class Users_Helpers():
    @staticmethod
    def hash_password(password: str):
        return password_hasher.hash(password)

    @staticmethod
    def reset_password(user_id: str, password: str):
        user_obj = Users_Methods.get_user_by_id(user_id)
        pass_hash = Users_Helpers.hash_password(password)
        user_obj.user_password = pass_hash
        return Users_Methods.update_user(user_obj)

    @staticmethod
    def check_unique_email(email):
        email = email.lower()
        try:
            Users_Methods.get_user_by_email(email)
            return False
        
        except Exception as e:
            print(f"Unable to retrieve email {email} from the database: {e}")
            return True
        
    @staticmethod
    def check_valid_user_type(type_id):
        try:
            UserTypes_Methods.get_type_by_id(type_id)
            return True
        
        except Exception as e:
            print(f"Unable to retrieve type ID {type_id} from the database: {e}")
            return False
    
    @staticmethod
    def validate_user_password(user_id, password):
        user_passhash = Users_Methods.get_user_by_id(user_id).user_password
        try:
            return password_hasher.verify(hash=user_passhash, password=password)
        except ArgonExceptions.VerifyMismatchError:
            return False
        except Exception as e:
            print(f"Unable to verify password for user ID {user_id}: {e}")
            return False
        
    @staticmethod
    def is_user_admin(user_id: int = None, user_email: str = None):
        user_email = user_email.lower()
        admin_role = UserTypes_Methods.get_type_by_name("Admin").type_id

        if not user_id == None:
            user_role = Users_Methods.get_user_by_id(user_id).type_id

            if user_role == admin_role:
                return True
            else:
                return False
            
        elif not user_email == None:
            user_role = Users_Methods.get_user_by_email(user_email).type_id
            
            if user_role == admin_role:
                return True
            else:
                return False
            
        else:
            return False