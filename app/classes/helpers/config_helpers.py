from app.classes.models.config import Config_Methods

from app.classes.helpers.shared_helpers import Helpers

class Config_Helpers:
    @staticmethod
    def get_latest_config():
        return Config_Methods.get_config_by_id(Config_Methods.get_all_configs()[0])
    
    @staticmethod
    def get_secret_value():
        return Config_Helpers.get_latest_config().secret_value
    
    @staticmethod
    def is_min_bid_percent():
        return Config_Helpers.get_latest_config().min_bid_percent
    
    @staticmethod
    def get_min_bid_amount():
        return Config_Helpers.get_latest_config().min_bid_amount
    
    @staticmethod
    def get_entity_name():
        return Config_Helpers.get_latest_config().entity_name
    
    @staticmethod
    def get_entity_logo():
        return Config_Helpers.get_latest_config().entity_logo
    
    @staticmethod
    def get_primary_color():
        return Config_Helpers.get_latest_config().primary_color
    
    @staticmethod
    def get_secondary_color():
        return Config_Helpers.get_latest_config().secondary_color
    
    @staticmethod
    def get_stripe_api_key():
        return Config_Helpers.get_latest_config().stripe_api_key
    
    @staticmethod
    def update_secret():
        latest_config = Config_Helpers.get_latest_config()
        latest_config.secret_value = Helpers.generate_secret()
        return Config_Methods.update_config(latest_config)