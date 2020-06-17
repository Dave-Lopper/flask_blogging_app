# test/unit/test_like_endpoints.py
from app.models import Post, User, Like


def test_like_endpoint_works_correctly(
        test_client, db_init, insert_user, insert_post, login_user):
    """
        GIVEN 1 user, 1 post
        WHEN like endpoint is hit for this post and user
        THEN - user has been redirected to the index
             - 1 like in db
    """
    user = User.query.first()
    post = Post.query.first()
    response = test_client.get(
        f"/like_post/{post.id}/{user.id}"
    )
    assert Like.query.count() == 1
    like = Like.query.first()
    assert like.post_id == post.id
    assert like.user_id == user.id
    assert response.location.endswith('/')


def test_like_endpoint_handes_404(test_client, db_init, insert_user,
                                  login_user):
    """
        GIVEN One logged-in user
        WHEN like endpoint is hit for unexisting post and user
        THEN - response's status code is 404
             - 404.j2.html is rendered
    """
    resp = test_client.get(
        "/like_post/9999/9999"
    )
    assert resp.status_code == 404
    assert b"404" in resp.data
    assert b"Not found" in resp.data
    assert b'Let&apos;s head back to <a href="/">the index</a>.' in resp.data


def test_unlike_endpoint_works_correctly(
        test_client, db_init, insert_user, insert_post, login_user):
    """
        GIVEN 1 user, 1 post, 1 like
        WHEN unlike endpoint is hit for this post and user
        THEN - user has been redirected to the index
             - no like in db
    """
    user = User.query.first()
    post = Post.query.first()
    like = Like(post_id=post.id, user_id=user.id)
    db_init.session.add(like)
    db_init.session.commit()

    response = test_client.get(
        f"/unlike_post/{post.id}/{user.id}"
    )
    assert response.location.endswith('/')
    assert Like.query.count() == 0


def test_unlike_endpoint_handes_404(test_client, db_init, insert_user,
                                    login_user):
    """
        GIVEN One logged-in user
        WHEN unlike endpoint is hit for unexisting post and user
        THEN - response's status code is 404
             - 404.j2.html is rendered
    """
    resp = test_client.get(
        "/unlike_post/9999/9999"
    )
    assert resp.status_code == 404
    assert b"404" in resp.data
    assert b"Not found" in resp.data
    assert b'Let&apos;s head back to <a href="/">the index</a>.' in resp.data


def test_like_redirects_referrer(test_client, db_init, insert_user,
                                 login_user, insert_post):
    """
        GIVEN One logged-in user and one post
        WHEN unlike endpoint is hit with referrer
        THEN redirection on referrer
    """
    user = User.query.first()
    post = Post.query.first()
    response = test_client.get(f"/like_post/{post.id}/{user.id}", headers={
        "Referer": f"http://localhost/user/{user.id}"
    })
    assert response.location == f"http://localhost/user/{user.id}"


def test_unlike_redirects_referrer(test_client, db_init, insert_user,
                                   login_user, insert_post):
    """
        GIVEN One logged-in user and one post
        WHEN unlike endpoint is hit with referrer
        THEN redirection on referrer
    """
    user = User.query.first()
    post = Post.query.first()
    like = Like(user_id=user.id, post_id=post.id, user=user, post=post)
    db_init.session.add(like)
    db_init.session.commit()

    response = test_client.get(f"/unlike_post/{post.id}/{user.id}", headers={
        "Referer": f"http://localhost/user/{user.id}"
    })
    assert response.location == f"http://localhost/user/{user.id}"
