import peewee

db_proxy = peewee.DatabaseProxy()

class BaseModel(peewee.Model):
    class Meta:
        db = db_proxy