# /manage.py
from dotenv import load_dotenv
from flask_migrate import Migrate

from app.blueprints import main, auth
from app.boot import create_app, DB
from app.models import *

load_dotenv(".env")

app = create_app()
migrate = Migrate(app, DB)
app.register_blueprint(auth)
app.register_blueprint(main)


if __name__ == "__main__":
    app.run()
