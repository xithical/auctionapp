import uuid

class Helpers:
    @staticmethod
    def create_uuid():
        return str(uuid.uuid4())