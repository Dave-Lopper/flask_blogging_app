# test/functional/test_user_registration.py
import datetime

from werkzeug.security import check_password_hash

from app.models import User


user = {
    "email": "valid_email@provider.com",
    "first_name": "Dave",
    "last_name": "Lopper",
    "password": "ILovePineapplePizzas",
    "birth_date": datetime.datetime.strptime(
        "05-07-1995",
        "%d-%m-%Y")
}


def test_email_is_verified_registration(test_client, db_init):
    invalid_emails = ["invalidemail.com", "invalid@email"]
    expected_flash = "Please provide a valid email adress"

    for email in invalid_emails:
        response = test_client.post(
            "/register",
            data={
                "signin_email": email,
                "signin_first_name": user["first_name"],
                "signin_last_name": user["last_name"],
                "signin_password": user["password"],
                "signin_password_confirm": user["password"],
                "signin_birth_data": user["birth_date"]})

        assert response.location.endswith("/signin")

        with test_client.session_transaction() as session:
            assert "email" in dict(session["_flashes"]).keys()
            assert dict(session["_flashes"])["email"] is not None
            assert dict(session["_flashes"])["email"] == expected_flash

    assert User.query.count() == 0


def test_user_password_is_verified_registration(test_client, db_init):
    password_confirm = "IdontLovePineapplePizzas"
    expected_flash = "Password and its confirmation are different !"
    response = test_client.post(
        "/register",
        data={
            "signin_email": user["email"],
            "signin_first_name": user["first_name"],
            "signin_last_name": user["last_name"],
            "signin_password": password_confirm,
            "signin_password_confirm": user["password"],
            "signin_birth_data": user["birth_date"]
        }
    )
    assert response.location.endswith("/signin")

    with test_client.session_transaction() as session:
        assert "password" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["password"] is not None
        assert dict(session["_flashes"])["password"] == expected_flash

    assert User.query.count() == 0


def test_user_is_registered_with_valid_data(test_client, db_init):
    response = test_client.post(
        "/register",
        data={
            "signin_email": user["email"],
            "signin_password": user["password"],
            "signin_password_confirm": user["password"],
            "signin_first_name": user["first_name"],
            "signin_last_name": user["last_name"],
            "signin_birth_date": user["birth_date"]
        }
    )

    assert response.location.endswith("/logged-in")
    assert User.query.count() == 1
    assert User.query.first().email == user["email"]
    assert User.query.first().first_name == user["first_name"]
    assert User.query.first().last_name == user["last_name"]
    assert User.query.first().birth_date == user["birth_date"]
    assert check_password_hash(User.query.first().password, user["password"])

    with test_client.session_transaction() as session:
        assert "_user_id" in session.keys()
        assert int(session["_user_id"]) == User.query.first().id
