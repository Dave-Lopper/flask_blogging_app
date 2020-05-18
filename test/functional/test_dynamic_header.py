# test/functional/test_dynamic_header.py
from app.models import User

index_link = b'<a href="/" class="mr-4">Index</a>'
logged_in_link = b'<a href="/logged-in" class="mr-4">Logged-in</a>'
logout_button = b'<a href="/logout">Logout</a>'


def test_index_link_does_not_show_on_index_page(
        test_client, db_init, insert_user):
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
        assert index_link not in response.data
        assert logged_in_link in response.data
        assert logout_button in response.data


def test_loggedin_link_does_not_show_on_loggedin_page(
        test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    with test_client.session_transaction():
        response = test_client.get("/logged-in")
        assert logged_in_link not in response.data
        assert index_link in response.data
        assert logout_button in response.data
