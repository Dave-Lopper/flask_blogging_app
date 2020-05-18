# test/functional/test_user_login.py
from app.models import User


expected_flash = "Please check your login details and try again."


def test_submitting_login_form_verfies_email(
        test_client, db_init, insert_user):
    user = User.query.first()
    response = test_client.post("/login", data={
        "login_email": "unexisting_email@gmail.com",
        "login_password": user.password
    })
    assert response.location.endswith("/")
    with test_client.session_transaction() as session:
        assert "message" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["message"] == expected_flash
        assert "_user_id" not in session.keys()


def test_submitting_login_form_verifies_password(
        test_client, db_init, insert_user):
    user = User.query.first()
    response = test_client.post("/login", data={
        "login_email": user.email,
        "login_password": "unexisting_password"
    })
    assert response.location.endswith("/")
    with test_client.session_transaction() as session:
        assert "message" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["message"] == expected_flash
        assert "_user_id" not in session.keys()


def test_submitting_login_with_valid_data_logs_in(
        test_client, db_init, insert_user):
    user = User.query.first()
    response = test_client.post("/login", data={
        "login_email": user.email,
        "login_password": "hardcoded_password"
    })
    assert response.location.endswith("/profile")

    with test_client.session_transaction() as session:
        assert "_user_id" in session.keys()
        assert int(session["_user_id"]) == user.id
        assert "_flashes" not in session.keys()
