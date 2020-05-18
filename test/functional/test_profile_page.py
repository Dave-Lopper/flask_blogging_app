# test/functional/test_profile_page.py
from app.models import User


def test_profile_page(test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    with test_client.session_transaction():
        response = test_client.get("/profile")
    assert response.status_code == 200
    assert b"Profile" in response.data
    assert b"this space is yours, here you can edit your profile&apos;s" \
        in response.data
    assert b"Edit profile" in response.data
    assert b"Email address" in response.data
    assert b"First name" in response.data
    assert b"Last name" in response.data
    assert b"Submit" in response.data
    assert b"Change password" in response.data
    assert bytes(user.email, encoding="utf8") in response.data
    assert bytes(user.first_name, encoding="utf8") in response.data
    assert bytes(user.last_name, encoding="utf8") in response.data
    assert b"Delete profile" in response.data
    assert b"Please confirm your password" in response.data
    assert b"I understand and want to delete my profile" in response.data
