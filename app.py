import os

from flask import Blueprint, Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


load_dotenv('.env')

DB = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config['ENV'] = os.getenv('ENV', 'dev')
DB.init_app(app)


home_bp = Blueprint('home', __name__)

@home_bp.route('/', defaults={'name': 'Dave Lopper'})
@home_bp.route('/<name>')
def home(name):
    return f"Hello {name} !"

app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run()