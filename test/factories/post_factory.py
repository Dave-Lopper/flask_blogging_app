# test/factories/user_factory.py
import factory

from app.boot import DB
from app.models import Post
from . import UserFactory


class PostFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Post
        sqlalchemy_session = DB.session
    content = factory.Faker('paragraph')
    user = factory.SubFactory(UserFactory)
    posted_at = factory.Faker('date_time')
