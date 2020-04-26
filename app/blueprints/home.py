# /app/blueprints/home.py
from flask import Blueprint

home_bp = Blueprint('home', __name__)


@home_bp.route('/', defaults={'name': 'Dave Lopper'})
@home_bp.route('/<name>')
def home(name):
    return f"Hello {name} !"
