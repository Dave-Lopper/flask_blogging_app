# test/conftest.py
import os

import pytest

from app.boot import create_app


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
