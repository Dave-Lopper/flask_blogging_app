# test/functional/test_user_registration.py
import datetime

from werkzeug.security import check_password_hash

from app.models import User
from test.factories import UserFactory


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
    """
    GIVEN set-up test client and applied migrations
    WHEN register is hit with invalid email
    THEN - Redirection on signin
         - Expected message is flashed in message category
         - No user is inserted
    """
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


def test_email_registration_existing_email(test_client, db_init):
    """
    GIVEN one inserted user
    WHEN register is hit with existing email
    THEN - Redirection on signin
         - Expected message is flashed in email category
         - No user is inserted
    """
    UserFactory.create(email="dave@lopper.com")
    expected_flash = "Email already exists"

    response = test_client.post(
        "/register",
        data={
            "signin_email": "dave@lopper.com",
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

    assert User.query.count() == 1


def test_user_password_is_verified_registration(test_client, db_init):
    """
    GIVEN set-up test client and applied migrations
    WHEN register is hit with password and confirmation not matching
    THEN - Redirection on signin
         - Expected message is flashed in message category
         - No user is inserted
    """
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
    """
    GIVEN set-up test client and applied migrations
    WHEN register is hit with valid data
    THEN - Redirection on profile
         - Expected message is flashed in message category
         - User is inserted in DB
         - User's attributes are correct
         - User is logged-in
    """
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

    assert response.location.endswith("/profile")
    assert User.query.count() == 1
    assert User.query.first().email == user["email"]
    assert User.query.first().first_name == user["first_name"]
    assert User.query.first().last_name == user["last_name"]
    assert User.query.first().birth_date == user["birth_date"]
    assert check_password_hash(User.query.first().password, user["password"])

    with test_client.session_transaction() as session:
        assert "_user_id" in session.keys()
        assert int(session["_user_id"]) == User.query.first().id
