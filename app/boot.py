# /app/boot.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


load_dotenv(".env")
DB = SQLAlchemy()


def create_app():
    app = Flask(__name__,
                template_folder=os.path.abspath("app/templates"))
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["ENV"] = os.getenv("ENV", "dev")
    app.secret_key = os.environ["SECRET_KEY"]
    DB.init_app(app)

    from app.models import User
    Migrate(app, DB)

    from .blueprints import auth, main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
