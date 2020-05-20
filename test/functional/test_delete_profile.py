# test/functional/test_delete_profile.py
from app.models import User


def test_delete_profile_checks_password(test_client, db_init, insert_user):
    expected_flash = "Please check your password and try again"
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )

    response = test_client.post(
        "/delete_profile",
        data={
            "delete_password": "wrong_password"
        }
    )

    assert response.location.endswith("/profile")

    with test_client.session_transaction() as session:
        assert "delete" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["delete"] is not None
        assert dict(session["_flashes"])["delete"] == expected_flash
        assert "_user_id" in session
        assert int(session["_user_id"]) == user.id


def test_delete_profile_deletes_user(test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )

    response = test_client.post(
        "/delete_profile",
        data={
            "delete_password": "hardcoded_password"
        }
    )

    assert response.location.endswith("/")

    with test_client.session_transaction() as session:
        assert "_flashes" not in session
        assert "_user_id" not in session

    assert User.query.count() == 0
