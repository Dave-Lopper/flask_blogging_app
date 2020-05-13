# test/unit/test_user_registration.py
import datetime

from app.boot import DB
from app.models import User


def test_register_endpoint_dont_accept_get_calls(test_client, db_init):
    response = test_client.get("/register")
    assert response.status_code == 405
    assert b"The method is not allowed for the requested URL." in response.data


def test_user_model_inserts_data_correctly(test_client, db_init):
    user = User(
        first_name="Dave",
        last_name="Lopper",
        email="dave@lopper.fr",
        password="hardcoded_unhashed_password",
        birth_date=datetime.datetime.strptime("05-07-1995", "%d-%m-%Y")
    )
    DB.session.add(user)
    DB.session.commit()
    assert User.query.count() == 1
    user_from_db = User.query.first()
    assert user_from_db.first_name == "Dave"
    assert user_from_db.last_name == "Lopper"
    assert user_from_db.email == "dave@lopper.fr"
    assert user_from_db.password == "hardcoded_unhashed_password"
    assert user_from_db.birth_date == datetime.datetime.strptime(
        "05-07-1995", "%d-%m-%Y"
    )
