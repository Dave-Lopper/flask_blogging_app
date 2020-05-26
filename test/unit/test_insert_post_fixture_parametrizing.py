# test/unit/test_insert_post_fixture_ parametrizing.py
import pytest

from app.models import Post


def test_fixture_insert_post_without_parameter(
        test_client, db_init, insert_post):
    """
    GIVEN 1 as parameter
    WHEN fixture insert_post is called
    THEN - One post has been inserted
         - The fixture has returned 1
    """
    assert insert_post == 1
    assert Post.query.count() == 1


@pytest.mark.parametrize("insert_post", [3], indirect=["insert_post"])
def test_fixture_insert_user_parameter_3(test_client, db_init, insert_post):
    """
    GIVEN 3 as parameter
    WHEN fixture insert_post is called
    THEN - Three posts has been inserted
         - The fixture has returned 3
    """
    assert insert_post == 3
    assert Post.query.count() == 3


@pytest.mark.parametrize("insert_post", [25], indirect=["insert_post"])
def test_fixture_insert_user_parameter_25(test_client, db_init, insert_post):
    """
    GIVEN 25 as parameter
    WHEN fixture insert_post is called
    THEN - 25 posts has been inserted
         - The fixture has returned 25
    """
    assert insert_post == 25
    assert Post.query.count() == 25
