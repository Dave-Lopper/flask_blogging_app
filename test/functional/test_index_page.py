# test/functional/test_index_page.py


def test_index_page(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    decoded_response = response.data.decode("utf-8")
    assert "Bloggin'" in decoded_response
    assert "Login'" in decoded_response
    assert "Email address" in decoded_response
    assert "Password" in decoded_response
    assert "Remember me ?" in decoded_response
    assert "Not with us yet ?" in decoded_response
