# test/functional/test_index_page.py


def test_index_page_unlogged(test_client, db_init):
    """
    GIVEN set-up test client
    WHEN index is hit
    THEN - Template is rendered correctly
         - Login form is included
         - Post form is not included
    """
    response = test_client.get("/")
    assert response.status_code == 200
    decoded_response = response.data.decode("utf-8")
    assert "Bloggin'" in decoded_response
    assert "Login'" in decoded_response
    assert "Email address" in decoded_response
    assert "Password" in decoded_response
    assert "Remember me ?" in decoded_response
    assert "Not with us yet ?" in decoded_response
    assert "Logout" not in decoded_response
    assert "How do you feel like today ?" not in decoded_response
    assert "Post" not in decoded_response


def test_index_page_logged(test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN index is hit
    THEN - Template is rendered correctly
         - Login form not included
         - Post form is included
    """
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
