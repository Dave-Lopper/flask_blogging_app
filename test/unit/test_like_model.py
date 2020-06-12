# test/unit/test_post_model.py
import datetime

from app.boot import DB
from app.models import User, Post, Like
from test.factories import PostFactory, UserFactory

posted_at = datetime.datetime.now()


def test_like_model_inserts_data_correctly(test_client, db_init, insert_user):
    """
    GIVEN one inserted post, two users
    WHEN Likes are inserted using model
    THEN - Likes are indeed inserted
         - Likes's attributes are correct
         - Relationship is bi-directionnal (likes can be retrieved from post)
    """
    first_user = User.query.first()
    post = PostFactory(user=first_user, user_id=first_user.id)
    like = Like(
        user=first_user,
        user_id=first_user.id,
        post=post,
        post_id=post.id
    )
    second_user = UserFactory.create()
    second_like = Like(
        user=second_user,
        user_id=second_user.id,
        post=post,
        post_id=post.id
    )
    DB.session.add_all([like, second_like, second_user])
    DB.session.commit()

    assert Like.query.count() == 2
    first_like = Like.query.filter(Like.user_id == first_user.id).first()
    assert first_like is not None
    assert first_like.post == post
    assert first_like.post_id == post.id
    second_like = Like.query.filter(Like.user_id == second_user.id).first()
    assert second_like is not None
    assert second_like.post == post
    assert second_like.post_id == post.id
    assert len(post.likes) == 2
    assert first_like in post.likes
    assert second_like in post.likes


def test_db_session_deletes_data_correctly(
        test_client, db_init, insert_post, insert_user):
    """
    GIVEN one inserted post and one user
    WHEN Like is deleted using DB object
    THEN Like is indeed missing from DB
    """
    post = Post.query.first()
    user = User.query.first()
    like = Like(post_id=post.id, user_id=user.id)
    DB.session.add(like)
    DB.session.commit()
    DB.session.query(Like) \
        .filter_by(post_id=post.id) \
        .filter_by(user_id=user.id) \
        .delete()
    assert Like.query.count() == 0
