# test/unit/test_post_model.py
import datetime

import pytest

from app.boot import DB
from app.models import User, Post, Like
from test.factories import PostFactory


content = """I'm baby umami tofu letterpress, portland farm - to - table
keffiyeh seitan. Air plant humblebrag live - edge vegan blue bottle
literally. Coloring book 3 wolf moon cliche, asynchronous pinterest pabst
cardigan direct trade scenester shabby chic mustache cornhole. Tousled cloud
bread heirloom cliche hashtag knausgaard cold - pressed butcher flannel.
Selvage sustainable raw denim craft beer.

Vexillologist bespoke leggings, cornhole tumeric readymade adaptogen
shoreditch mixtape meggings. Hashtag enamel pin sustainable locavore
lomo flexitarian snackwave. Tumeric tofu disrupt swag chia banjo
aesthetic man bun helvetica pug kickstarter migas retro prism."""
posted_at = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def test_post_model_inserts_data_correctly(test_client, db_init, insert_user):
    """
    GIVEN one inserted post
    WHEN Post is inserted using model
    THEN - Post is indeed inserted
         - Post's attributes are correct
    """
    post = Post(
        content=content,
        user=User.query.first(),
        user_id=User.query.first().id,
        posted_at=posted_at,
    )
    DB.session.add(post)
    DB.session.commit()
    assert Post.query.count() == 1
    post_from_db = Post.query.first()
    assert post_from_db.content == content
    assert post_from_db.posted_at == datetime.datetime.strptime(
        posted_at, "%Y-%m-%d %H:%M:%S")
    assert post_from_db.user_id == User.query.first().id
    assert post_from_db.user == User.query.first()


def test_user_model_updates_data_correctly(test_client, db_init, insert_post):
    """
    GIVEN one inserted post
    WHEN Post is updated using model
    THEN - Post's attributes are correctly updated in DB
    """
    post = Post.query.first()

    post.content = content
    DB.session.commit()
    assert DB.session.query(Post).get(post.id).content == content


def test_db_session_updates_data_correctly(test_client, db_init, insert_post):
    """
    GIVEN one inserted post
    WHEN Post is updated using DB object
    THEN - Post's attributes are correctly updated in DB
    """
    post = Post.query.first()

    DB.session.query(Post).filter_by(id=post.id).update(
        {
            "content": content
        }
    )
    DB.session.commit()
    assert DB.session.query(Post).get(post.id).content == content


def test_db_session_deletes_data_correctly(test_client, db_init, insert_post):
    """
    GIVEN one inserted post
    WHEN Post is deleted using DB object
    THEN Post is indeed missing from DB
    """
    post = Post.query.first()
    DB.session.query(Post).filter_by(id=post.id).delete()
    assert Post.query.count() == 0


def test_hybrid_attribute_excerpt_has_expected_behaviour(test_client, db_init):
    """
    GIVEN applied migrations
    WHEN one post is inserted
    THEN - post's excerpt is corresponds to the 180 first characters of the
    content + ...
         - post's excerpt length is equal or less than 180 chars
    """
    post = PostFactory.create(content=content)
    excerpt_words = content[:177].split(' ')
    excerpt_words.pop(len(excerpt_words) - 1)
    expected_excerpt = f"{' '.join(excerpt_words)}..."

    assert post.excerpt == expected_excerpt
    assert len(post.excerpt) <= 180


@pytest.mark.parametrize("insert_user", [3], indirect=["insert_user"])
def test_hybrid_attribute_users_liked(test_client, db_init, insert_user,
                                      insert_post):
    """
    GIVEN one inserted post, three inserted users
    THEN post hybrid attribute is empty
    WHEN three likes are inserted for that post
    THEN post hybrid attribute has the expected values
         (IDs of the users who liked)
    """
    users = User.query.all()
    post = Post.query.first()
    assert post.likes == []
    assert post.users_liked == []
    for user in users:
        db_init.session.add(Like(user_id=user.id, post_id=post.id))
    db_init.session.commit()
    assert len(post.users_liked)
    for user in users:
        assert user.id in post.users_liked
