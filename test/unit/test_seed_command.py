# test/unit/test_seed_command.py
from app.models import Post, User
from app.blueprints.post import seed


def test_seed_command(cli_tester):
    """
    GIVEN applied migrations
    WHEN seed command is executed
    THEN expected output is returned, data is inserted
    """
    runner = cli_tester[2]
    result = runner.invoke(seed, input="50\n1")
    assert "Working on it..." in result.output
    assert "Inserted 50 users and 50 posts in database." in result.output
    assert User.query.count() == 50
    assert Post.query.count() == 50


def test_seed_command_second_case(cli_tester):
    """
    GIVEN applied migrations
    WHEN seed command is executed
    THEN expected output is returned, data is inserted
    """
    runner = cli_tester[2]
    result = runner.invoke(seed, input="25\n3")
    assert "Working on it..." in result.output
    assert "Inserted 25 users and 75 posts in database." in result.output
    assert User.query.count() == 25
    assert Post.query.count() == 75
