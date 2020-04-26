# /app/boot.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .blueprints import home_bp


load_dotenv(".env")
DB = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        os.environ["SQLALCHEMY_DATABASE_URI"]
    app.config["ENV"] = os.getenv("ENV", "dev")
    DB.init_app(app)

    app.register_blueprint(home_bp)

    return app
