# test/functional/test_change_password_page.py
from app.models import User


def test_change_password_page(test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    with test_client.session_transaction():
        response = test_client.get("/profile/change_password")
    assert response.status_code == 200
    assert b"Change password" in response.data
    assert b"Current password" in response.data
    assert b"New password" in response.data
    assert b"Confirm new password" in response.data
    assert b"Submit" in response.data
    assert b"Profile" in response.data
