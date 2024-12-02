import uuid
import string
import random
import secrets

class Helpers:
    @staticmethod
    def create_uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    def create_event_code():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(6))
    
    @staticmethod
    def generate_secret():
        secret = secrets.token_urlsafe(32)
        return secret