# test/unit/test_insert_user_fixture_ parametrizing.py
import pytest

from app.models import User


@pytest.mark.parametrize("insert_user", [1], indirect=["insert_user"])
def test_fixture_insert_user_parameter_1(test_client, db_init, insert_user):
    assert insert_user == 1
    assert User.query.count() == 1


@pytest.mark.parametrize("insert_user", [3], indirect=["insert_user"])
def test_fixture_insert_user_parameter_3(test_client, db_init, insert_user):
    assert insert_user == 3
    assert User.query.count() == 3


@pytest.mark.parametrize("insert_user", [25], indirect=["insert_user"])
def test_fixture_insert_user_parameter_25(test_client, db_init, insert_user):
    assert insert_user == 25
    assert User.query.count() == 25
