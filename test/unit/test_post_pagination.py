# test/unit/test_post_pagination.py
import os

from click.testing import CliRunner

from app.blueprints.post import seed


def test_current_page_is_one_by_default(cli_tester):
    """
        GIVEN 150 posts, 50 users inserted
        WHEN index is hit
        THEN page 1 button in disabled
    """
    runner = cli_tester[2]
    test_client = cli_tester[0].test_client()
    runner.invoke(seed, input="50\n3")

    response = test_client.get("/")
    assert b'<li class="page-item disabled" test="1">' in response.data


def test_previous_button_is_disabled_on_page_one(cli_tester):
    """
        GIVEN 150 posts, 50 users inserted
        WHEN index is hit
        THEN previous button in disabled
    """
    runner = cli_tester[2]
    test_client = cli_tester[0].test_client()
    runner.invoke(seed, input="50\n3")

    response = test_client.get("/?page=1")
    assert b'<li class="page-item disabled" test="previous">' in response.data


def test_next_button_is_disabled_on_last_page(cli_tester):
    """
        GIVEN 120 posts, 40 users inserted
        WHEN index is hit, page 6 (last page)
        THEN next button in disabled
    """
    runner = cli_tester[2]
    test_client = cli_tester[0].test_client()
    runner.invoke(seed, input="40\n3")

    response = test_client.get("/?page=6")
    assert b'<li class="page-item disabled" test="next">' in response.data


def test_page_show(cli_tester):
    """
        GIVEN 800 posts, 20 users inserted
        WHEN index is hit on page 10 (out of 40)
        THEN - Skipped pages are hidden (6 and 36)
             - ... button is present and disabled
    """
    runner = cli_tester[2]
    test_client = cli_tester[0].test_client()
    runner.invoke(seed, input="20\n40")

    response = test_client.get("/?page=10")
    assert b'<li class="page-item disabled" test="...">' in response.data
    assert b'<li class="page-item" test="6">' not in response.data
    assert b'<li class="page-item" test="36">' not in response.data
    assert b'<li class="page-item disabled" test="6">' not in response.data
    assert b'<li class="page-item disabled" test="36">' not in response.data


def test_pagination_margin_logged(
        test_client, db_init, insert_user, login_user):
    """
        GIVEN 800 posts, 20 users inserted, logged-in user
        WHEN index is hit
        THEN the margin class is present on pagination container
    """
    db_test = "{}_test".format(os.environ["SQLALCHEMY_DATABASE_URI"])
    runner = CliRunner(
        env={"SQLALCHEMY_DATABASE_URI": db_test}
    )
    runner.invoke(seed, input="20\n40")
    response = test_client.get("/")
    assert b'<div class="row paginationContainer">' in response.data


def test_pagination_margin_unlogged(cli_tester):
    """
        GIVEN 800 posts, 20 users inserted, unlogged user
        WHEN index is hit
        THEN the margin class is not present on pagination container
    """
    runner = cli_tester[2]
    test_client = cli_tester[0].test_client()
    runner.invoke(seed, input="20\n40")
    response = test_client.get("/")
    assert b'<div class="row paginationContainer">' not in response.data
