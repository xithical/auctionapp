import uuid
import string
import random

class Helpers:
    @staticmethod
    def create_uuid():
        return str(uuid.uuid4())
    
    @staticmethod
    def create_event_code():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(6))