# test/functional/test_post_writing.py
from app.models import Post


content = """I'm baby umami tofu letterpress, portland farm - to - table
keffiyeh seitan. Air plant humblebrag live - edge vegan blue bottle
literally. Coloring book 3 wolf moon cliche, asynchronous pinterest pabst
cardigan direct trade scenester shabby chic mustache cornhole. Tousled cloud
bread heirloom cliche hashtag knausgaard cold - pressed butcher flannel.
Selvage sustainable raw denim craft beer."""


def test_write_post_endpoint_inserts_post(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN /write post is hit
    THEN - Redirection on index
    - Post is inserted
    - Inserted post has the expected content
    """
    response = test_client.post(
        "/write_post",
        data={
            "write_post_content": content
        }
    )
    assert response.location.endswith("/")
    assert Post.query.count() == 1
    assert Post.query.first().content == content
