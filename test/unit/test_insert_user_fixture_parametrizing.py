# test/unit/test_insert_user_fixture_ parametrizing.py
import pytest

from app.models import User


@pytest.mark.parametrize("insert_user", [1], indirect=["insert_user"])
def test_fixture_insert_user_parameter_1(test_client, db_init, insert_user):
    """
    GIVEN 1 as parameter
    WHEN fixture insert_user is called
    THEN - One user has been inserted
         - The fixture has returned 1
    """
    assert insert_user == 1
    assert User.query.count() == 1


@pytest.mark.parametrize("insert_user", [3], indirect=["insert_user"])
def test_fixture_insert_user_parameter_3(test_client, db_init, insert_user):
    """
    GIVEN 3 as parameter
    WHEN fixture insert_user is called
    THEN - Three users has been inserted
         - The fixture has returned 3
    """
    assert insert_user == 3
    assert User.query.count() == 3


@pytest.mark.parametrize("insert_user", [25], indirect=["insert_user"])
def test_fixture_insert_user_parameter_25(test_client, db_init, insert_user):
    """
    GIVEN 25 as parameter
    WHEN fixture insert_user is called
    THEN - 25 users has been inserted
         - The fixture has returned 25
    """
    assert insert_user == 25
    assert User.query.count() == 25
