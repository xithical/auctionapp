from app.classes.models.base_model import db_proxy

from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.init_helpers import Init_Helpers

from app.classes.frontend.web import app

if __name__ == "__main__":    
    Init_Helpers.init_db()

    app.run()

    exit()