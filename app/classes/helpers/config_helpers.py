from app.classes.models.config import Config_Methods

class Config_Helpers:
    def get_latest_config():
        latest_config_id = Config_Methods.get_all_configs()[0].entry_id
        return Config_Methods.get_config_by_id(latest_config_id)