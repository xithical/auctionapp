from peewee import (
    AutoField,
    CharField
)
from playhouse import model_to_dict

# Models import
from app.classes.models.base_model import BaseModel

# Helpers import
from app.classes.helpers.db_helpers import DatabaseHelpers

# Item Donors Model
class ItemDonors(BaseModel):
    donor_id = AutoField(primary_key=True, unique=True)
    donor_firstname = CharField(max_length = 45)
    donor_lastname = CharField(max_length = 45)
    donor_email = CharField(max_length = 255)
    donor_phone = CharField(max_length = 20)
    company_name = CharField(max_length = 50, null = True)

    class Meta:
        table_name = "ItemDonors"

class ItemDonors_Methods:
    def __init__(self, database):
        self.database = database

    @staticmethod
    def create_donor(
        donor_firstname: str,
        donor_lastname: str,
        donor_email: str,
        donor_phone: str,
        company_name: str = None
    ) -> int:
        """
        Creates item donor record in the database

        Args:
            donor_firstname: The first name of the donor
            donor_lastname: The last name of the donor
            donor_email: The email address of the donor
            donor_phone: The phone number of the donor
            company_name: The company name of the donor (optional)

        Returns:
            int: The numeric ID of the donor

        Raises:
            PeeweeException: If the donor ID already exists
        """
        return ItemDonors.create(
            donor_firstname=donor_firstname,
            donor_lastname=donor_lastname,
            donor_email=donor_email,
            donor_phone=donor_phone,
            company_name=company_name
        ).donor_id
    
    @staticmethod
    def get_all_donors():
        query = ItemDonors.select()
        return DatabaseHelpers.get_rows(query)
    
    @staticmethod
    def get_donor_by_id(donor_id: int):
        return ItemDonors.select().where(ItemDonors.donor_id == donor_id).get()
    
    @staticmethod
    def update_donor(donor_obj: object):
        return donor_obj.save()
    
    @staticmethod
    def remove_donor(donor_id: int):
        ItemDonors.delete().where(ItemDonors.donor_id == donor_id).execute()
        return True