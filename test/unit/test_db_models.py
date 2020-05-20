# test/unit/test_db_models.py
import datetime

from app.boot import DB
from app.models import User

new_first_name = "Dave"
new_last_name = "Lopper"
new_email = "dave@lopper.com"


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


def test_user_model_updates_data_correctly(test_client, db_init, insert_user):
    user = User.query.first()

    user.first_name = new_first_name
    DB.session.commit()
    assert DB.session.query(User).get(user.id).first_name == new_first_name
    user.last_name = new_last_name
    DB.session.commit()
    assert DB.session.query(User).get(user.id).last_name == new_last_name
    user.email = new_email
    DB.session.commit()
    assert DB.session.query(User).get(user.id).email == new_email


def test_db_session_updates_data_correctly(test_client, db_init, insert_user):
    user = User.query.first()

    DB.session.query(User).filter_by(id=user.id).update(
        {
            "first_name": new_first_name,
            "last_name": new_last_name,
            "email": new_email
        }
    )
    DB.session.commit()
    assert DB.session.query(User).get(user.id).first_name == new_first_name
    assert DB.session.query(User).get(user.id).last_name == new_last_name
    assert DB.session.query(User).get(user.id).email == new_email
