# test/functional/test_edit_profile.py
from app.models import User


def test_email_is_verified_edit_profile(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN edit_profile is hit with invalid email address
    THEN - Redirection on profile
         - Expected message is flashed
         - User's attributes are unchanged
    """
    invalid_emails = ["invalidemail.com", "invalid@email"]
    expected_flash = "Please provide a valid email adress"

    for email in invalid_emails:
        response = test_client.post("/edit_profile", data={
            "edit_email": email,
            "edit_first_name": "Dave",
            "edit_last_name": "Lopper"
        })

        assert response.location.endswith("/profile")

        with test_client.session_transaction() as session:
            assert "edit" in dict(session["_flashes"]).keys()
            assert dict(session["_flashes"])["edit"] is not None
            assert dict(session["_flashes"])["edit"] == expected_flash

        assert User.query.get(login_user.id).first_name != "Dave"
        assert User.query.get(login_user.id).last_name != "Lopper"
        assert User.query.get(login_user.id).email != email


def test_email_is_edited_with_valid_data(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN edit_profile is hit with valid email
    THEN - No message is flashed
         - User has been changed
         - Updated attributes are visible on profile
    """
    response = test_client.post(
        "/edit_profile",
        data={
            "edit_email": "dave@lopper.com",
            "edit_first_name": "Dave",
            "edit_last_name": "Lopper"
        },
        follow_redirects=True
    )

    with test_client.session_transaction() as session:
        assert "_flashes" not in session.keys()

    assert User.query.get(login_user.id).first_name == "Dave"
    assert User.query.get(login_user.id).last_name == "Lopper"
    assert User.query.get(login_user.id).email == "dave@lopper.com"

    assert b"Dave" in response.data
    assert b"Lopper" in response.data
    assert b"dave@lopper.com" in response.data
