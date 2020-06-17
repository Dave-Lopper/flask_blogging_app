# test/functional/test_like_feature.py
from app.models import Post, User, Like


def test_like_button_does_not_show_for_unlogged_user(
        test_client, db_init, insert_post):
    """
        GIVEN 1 post
        WHEN index is hit unlogged
        THEN like button is not displayed
    """
    response = test_client.get("/")
    assert '<span id="like">' not in response.data.decode("utf-8")


def test_like_button_does_show_for_logged_user(
        test_client, db_init, insert_user, login_user, insert_post):
    """
        GIVEN 1 logged-in user and 1 post
        WHEN index is hit logged
        THEN like button is displayed
    """
    response = test_client.get("/")
    assert '<span id="like">' in response.data.decode("utf-8")


def test_like_endpoint_works_correctly(
        test_client, db_init, insert_user, insert_post, login_user):
    """
        GIVEN 1 user, 1 post
        WHEN like endpoint is hit for this post and user
        THEN Unlike button is displayed
    """
    user = User.query.first()
    post = Post.query.first()
    response = test_client.get(
        f"/like_post/{post.id}/{user.id}",
        follow_redirects=True
    )
    assert '<span id="unlike">' in response.data.decode("utf-8")


def test_unlike_endpoint_works_correctly(
        test_client, db_init, insert_user, insert_post, login_user):
    """
        GIVEN 1 user, 1 post, 1 like
        WHEN unlike endpoint is hit for this post and user
        THEN Like button is displayed
    """
    user = User.query.first()
    post = Post.query.first()
    like = Like(post_id=post.id, user_id=user.id)
    db_init.session.add(like)
    db_init.session.commit()

    response = test_client.get(
        f"/unlike_post/{post.id}/{user.id}",
        follow_redirects=True
    )
    assert '<span id="like">' in response.data.decode("utf-8")
