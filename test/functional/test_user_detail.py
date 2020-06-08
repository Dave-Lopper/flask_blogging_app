# test/functional/test_user_detail.py
from app.models import User
from test.factories import PostFactory


def test_user_posts_are_in_detail(test_client, db_init, insert_user):
    """
    GIVEN one inserted user, and five posts authored by the user
    WHEN user detail is hit
    THEN - Five post cards are in response
         - The five post's contents are present in the response
    """
    author = User.query.first()
    posts = []
    for i in range(5):
        post = PostFactory.create(user=author, user_id=author.id)
        posts.append(post)

    response = test_client.get(f"/user/{author.id}")
    assert str(response.data).count(
        '<div class="col-10 offset-1 card p-3 mb-3">'
    ) == 5
    for post in posts:
        assert post.content in str(response.data.decode("utf-8"))


def test_unexisting_user_detail_returns_404_template(test_client, db_init):
    """
    GIVEN test_client and db init
    WHEN user detail is hit with unexisting user id
    THEN - Response status code is 404
         - 404.j2.html is rendered
    """
    resp = test_client.get("/user/999")
    assert resp.status_code == 404
    assert b"404" in resp.data
    assert b"Not found" in resp.data
    assert b'Let&apos;s head back to <a href="/">the index</a>.' in resp.data
