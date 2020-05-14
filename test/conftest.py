# test/conftest.py
import os

import pytest

from app.boot import create_app, DB
from .factories import UserFactory


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
