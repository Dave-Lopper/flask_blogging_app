# test/unit/test_post_writing.py


def test_edit_profile_endpoint_dont_accept_get_calls(test_client, db_init):
    """
    GIVEN set-up test client and applied migrations
    WHEN post_writing in hit with GET method
    THEN - Response code is 405
         - Response message matches expectation
    """
    response = test_client.get("/write_post")
    assert response.status_code == 405
    assert b"The method is not allowed for the requested URL." in response.data
