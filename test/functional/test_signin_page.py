# test/functional/test_signin_page.py


def test_signin_page(test_client):
    response = test_client.get("/signin")
    assert response.status_code == 200
    decoded_response = response.data.decode("utf-8")
    assert "Not with us yet ?" in decoded_response
    assert "Create your account and blog with us !" in decoded_response
    assert "Email address" in decoded_response
    assert "First name" in decoded_response
    assert "Last name" in decoded_response
    assert "Birth date" in decoded_response
    assert "Password" in decoded_response
    assert "Confirm password" in decoded_response
    assert "Already have an account ?" in decoded_response
    assert "Log-in'" in decoded_response
    assert "to blog !" in decoded_response
    assert "Submit" in decoded_response
