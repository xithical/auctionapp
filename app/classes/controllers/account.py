from app.classes.helpers.users_helpers import Users_Helpers

from app.classes.models.users import Users_Methods

class Account_Controller:
    @staticmethod
    def list_user_details(user_id: str):
        output = {}
        
        user = Users_Methods.get_user_by_id(user_id)
        
        output["user_firstname"] = user.user_firstname
        output["user_lastname"] = user.user_lastname
        output["user_email"] = user.user_email
        output["user_phone"] = user.user_phone
        
        return output
    
    @staticmethod
    def update_user_details(
        user_id: str,
        user_firstname: str = None,
        user_lastname: str = None,
        user_email: str = None,
        user_phone: str = None
    ):
        user = Users_Methods.get_user_by_id(user_id)

        if user_firstname is not None:
            user.user_firstname = user_firstname
        if user_lastname is not None:
            user.user_lastname = user_lastname
        if user_email is not None:
            user.user_email = user_email
        if user_phone is not None:
            user.user_phone = user_phone

        return Users_Methods.update_user(user)
    
    @staticmethod
    def reset_password(
        user_id: str,
        old_pass: str,
        new_pass: str
    ):
        if Users_Helpers.validate_user_password(user_id, old_pass):
            if old_pass == new_pass:
                return False
            try:
                Users_Helpers.reset_password(user_id, new_pass)
                return True
            except Exception as e:
                print(f"Error resetting password for user {user_id}: {e}")
                return False
        else:
            return False