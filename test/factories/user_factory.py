# test/factories/user_factory.py
import datetime

import factory
from werkzeug.security import generate_password_hash

from app.boot import DB
from app.models import User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = DB.session
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(
        lambda x: f"{x.first_name.lower()}.{x.last_name.lower()}@gmail.com"
    )
    birth_date = factory.Faker('date_time')
    password = generate_password_hash("hardcoded_password")
    registered_at = datetime.datetime.now()
