# test/unit/test_post_user_association.py
from app.models import Post, User


content = """I'm baby umami tofu letterpress, portland farm - to - table
keffiyeh seitan. Air plant humblebrag live - edge vegan blue bottle
literally. Coloring book 3 wolf moon cliche, asynchronous pinterest pabst
cardigan direct trade scenester shabby chic mustache cornhole. Tousled cloud
bread heirloom cliche hashtag knausgaard cold - pressed butcher flannel.
Selvage sustainable raw denim craft beer."""


def test_post_user_association_factories(
        test_client, db_init, insert_post):
    """
    GIVEN test client and applied migrations
    WHEN post is inserted using fixture
    THEN - User is inserted as well
    - Association fields are correct on both sides
    """
    assert User.query.count() == 1

    user = User.query.first()
    post = Post.query.first()

    assert post.user == user
    assert post.user_id == user.id
    assert len(user.posts) == 1
    assert user.posts[0] == post


def test_post_user_association_endpoint(
        test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN post is inserted using /write_post endpoint
    THEN association fields are correct on both sides
    """
    test_client.post(
        "/write_post",
        data={
            "write_post_content": content
        }
    )
    user = User.query.first()
    post = Post.query.first()
    assert post.user == user
    assert post.user_id == user.id
    assert len(user.posts) == 1
    assert user.posts[0] == post
