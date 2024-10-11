from argon2 import PasswordHasher

from app.classes.models.users import Users_Methods

class Users_Helpers():
    @staticmethod
    def hash_password(password: str):
        return PasswordHasher.hash(password)

    @staticmethod
    def reset_password(self, user_id: str, password: str):
        user_obj = Users_Methods.get_user_by_id(user_id)
        pass_hash = Users_Helpers.hash_password(password)
        user_obj.user_password = pass_hash
        return Users_Methods.update_user(user_obj)