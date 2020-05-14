# test/functional/test_index_page.py
from app.models import User


def test_index_page_unlogged(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    decoded_response = response.data.decode("utf-8")
    assert "Bloggin'" in decoded_response
    assert "Login'" in decoded_response
    assert "Email address" in decoded_response
    assert "Password" in decoded_response
    assert "Remember me ?" in decoded_response
    assert "Not with us yet ?" in decoded_response


def test_index_page_logged(test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    with test_client.session_transaction():
        response = test_client.get("/")
    assert response.status_code == 200
    decoded_response = response.data.decode("utf-8")
    assert "Bloggin'" in decoded_response
    assert "Logout" in decoded_response
    assert "Login'" not in decoded_response
    assert "Email address" not in decoded_response
    assert "Password" not in decoded_response
    assert "Remember me ?" not in decoded_response
    assert "Not with us yet ?" not in decoded_response
