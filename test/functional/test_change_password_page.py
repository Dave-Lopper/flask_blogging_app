# test/functional/test_change_password_page.py


def test_change_password_page(test_client, db_init, insert_user, login_user):
    response = test_client.get("/profile/change_password")
    assert response.status_code == 200
    assert b"Change password" in response.data
    assert b"Current password" in response.data
    assert b"New password" in response.data
    assert b"Confirm new password" in response.data
    assert b"Submit" in response.data
    assert b"Profile" in response.data
