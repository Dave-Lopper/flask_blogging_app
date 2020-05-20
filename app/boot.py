
# pylint: disable=import-outside-toplevel
# /app/boot.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
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

    from .blueprints import auth, main, profile
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(profile)

    login_manager = LoginManager()
    login_manager.login_view = "main.index"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
