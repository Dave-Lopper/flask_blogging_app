# /app/models/user.py
from sqlalchemy import DateTime

from ..boot import DB


class User(DB.Model):
    __tablename__ = 'users'
    id = DB.Column(DB.Integer, primary_key=True, nullable=False)
    email = DB.Column(DB.String(150), unique=True)
    password = DB.Column(DB.String(100))
    first_name = DB.Column(DB.String(50))
    last_name = DB.Column(DB.String(50))
    birth_date = DB.Column(DateTime)
    registered_at = DB.Column(DateTime)
