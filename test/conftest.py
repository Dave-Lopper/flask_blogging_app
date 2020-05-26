# test/conftest.py
import os

import pytest

from app.boot import create_app, DB
from app.models import User
from .factories import UserFactory, PostFactory


@pytest.fixture
def test_client():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "{}_test".format(os.environ["SQLALCHEMY_DATABASE_URI"])
    app.config["TESTING"] = True
    ctx = app.app_context()
    ctx.push()
    yield app.test_client()
    ctx.pop()


@pytest.fixture
def db_init():
    DB.create_all()
    yield DB
    DB.session.close()
    DB.drop_all()


@pytest.fixture
def insert_user(request):
    if hasattr(request, "param"):
        UserFactory.create_batch(request.param)
        return request.param
    else:
        UserFactory.create()
        return 1


@pytest.fixture
def insert_post(request):
    if hasattr(request, "param"):
        PostFactory.create_batch(request.param)
        return request.param
    else:
        PostFactory.create()
        return 1


@pytest.fixture
def login_user(test_client):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    return user
