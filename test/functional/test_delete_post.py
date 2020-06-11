# test/functional/test_delete_post.py
from app.models import Post
from test.factories import PostFactory, UserFactory


def test_post_deletion(test_client, db_init, insert_user, login_user):
    """
        GIVEN one inserted and logged-in user and one post
        WHEN delete_post is hit
        THEN - Post has been deleted
             - User is redirected on user detail
             - Expected message is flashed
    """
    expected_flash = "Post deleted succesfully"
    post = PostFactory.create(user=login_user, user_id=login_user.id)
    db_init.session.commit()
    response = test_client.get(
        f"/delete_post/{post.id}",
        follow_redirects=True
    )
    assert Post.query.count() == 0
    assert len(login_user.posts) == 0
    assert login_user.first_name in response.data.decode("utf-8")
    assert login_user.last_name in response.data.decode("utf-8")
    assert expected_flash in response.data.decode("utf-8")


def test_post_deletion_404(test_client, db_init, insert_user, login_user):
    """
        GIVEN one inserted and logged-in user
        WHEN delete_post is hit with unexisting post id
        THEN - Response status code is 404
             - 404.j2.html is rendered
    """
    resp = test_client.get("/delete_post/999")
    assert resp.status_code == 404
    assert b"404" in resp.data
    assert b"Not found" in resp.data
    assert b'Let&apos;s head back to <a href="/">the index</a>.' in resp.data


def test_delete_button_dont_appear_on_other_users_page(
        test_client, db_init, insert_user, login_user):
    """
        GIVEN one inserted and logged-in user
        WHEN browsing another's user page
        THEN delete button is not displayed
    """
    second_user = UserFactory.create()
    db_init.session.commit()
    response = test_client.get(f"/user/{second_user.id}")
    assert "Delete post" not in response.data.decode("utf-8")
