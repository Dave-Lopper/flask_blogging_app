# test/functional/test_dynamic_header.py

index_link = b'<a href="/" class="mr-4">Index</a>'
profile_link = b'<a href="/profile" class="mr-4">Profile</a>'
logout_button = b'<a href="/logout">Logout</a>'


def test_index_link_does_not_show_on_index_page(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN index is hit
    THEN - Index link is not rendered
         - Profile link is
         - Logout link is
    """
    response = test_client.get("/")
    assert index_link not in response.data
    assert profile_link in response.data
    assert logout_button in response.data


def test_profile_link_does_not_show_on_profile_page(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN profile is hit
    THEN - Index link is rendered
         - Profile link is not
         - Logout link is
    """
    response = test_client.get("/profile")
    assert profile_link not in response.data
    assert index_link in response.data
    assert logout_button in response.data


def test_profile_link_shows_on_change_password_page(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN profile/change_password is hit
    THEN - Index link is rendered
         - Profile link is too
         - Logout link is too
    """
    response = test_client.get("/profile/change_password")
    assert profile_link in response.data
    assert index_link in response.data
    assert logout_button in response.data
