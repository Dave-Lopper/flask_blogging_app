# test/functional/test_feed.py
import datetime

from app.models import Post, User


def test_feed_logged_post(test_client, db_init, insert_user, login_user):
    """
    GIVEN one logged-in user
    WHEN index is hit
    THEN - Login form not included
         - Post form is included
    """
    now = datetime.datetime.now()
    user = User.query.first()
    post = Post(content="Test post content",
                posted_at=now,
                user=user,
                user_id=user.id)
    db_init.session.add(post)
    db_init.session.commit()
    response = test_client.get("/")

    assert response.status_code == 200
    assert bytes(
        f"{user.first_name} {user.last_name}",
        encoding="utf-8"
    ) in response.data
    assert bytes(now.strftime("% d % b, % Y"), encoding="utf-8")
    assert b"Test post content" in response.data


def test_index_page_unlogged_post(test_client, db_init, insert_user):
    """
    GIVEN set-up test client
    WHEN index is hit
    THEN - Login form is included
         - Post form is not included
    """
    now = datetime.datetime.now()
    user = User.query.first()
    post = Post(content="Test post content",
                posted_at=now,
                user_id=user.id,
                user=user)
    db_init.session.add(post)
    db_init.session.commit()
    response = test_client.get("/")

    assert response.status_code == 200
    assert bytes(
        f"{user.first_name} {user.last_name}",
        encoding="utf-8"
    ) in response.data
    assert bytes(now.strftime("% d % b, % Y"), encoding="utf-8")
    assert b"Test post content" in response.data
