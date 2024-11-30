from app.classes.helpers.config_helpers import Config_Helpers
from app.classes.helpers.init_helpers import Init_Helpers

from app.classes.frontend.web import app

# Run init tasks
Init_Helpers.init_db()
app.config["SECRET_KEY"] = Config_Helpers.get_secret_value()

# Run the app
if __name__ == "__main__":    

    app.run()

    # Terminate when the app stops running
    exit()