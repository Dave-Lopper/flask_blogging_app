# test/functional/test_password_change.py


def test_change_password_endpoint_checks_current_password(
        test_client, db_init, insert_user, login_user):
    expected_flash = "Please check your password and try again"
    response = test_client.post(
        "/edit_password",
        data={
            "edit_current_password": "wrong_password",
            "edit_new_password": "new_password",
            "edit_new_password_confirm": "new_password"
        }
    )
    assert response.location.endswith("/profile/change_password")

    with test_client.session_transaction() as session:
        assert "current" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["current"] is not None
        assert dict(session["_flashes"])["current"] == expected_flash


def test_change_password_endpoint_checks_new_password_confirm(
        test_client, db_init, insert_user, login_user):
    expected_flash = "The new password and its confirmation don't match"
    response = test_client.post(
        "/edit_password",
        data={
            "edit_current_password": "hardcoded_password",
            "edit_new_password": "new_password",
            "edit_new_password_confirm": "new_password_not_matching"
        }
    )
    assert response.location.endswith("/profile/change_password")

    with test_client.session_transaction() as session:
        assert "new" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["new"] is not None
        assert dict(session["_flashes"])["new"] == expected_flash


def test_change_password_endpoint_works_correctly_with_valid_data(
        test_client, db_init, insert_user, login_user):
    expected_flash = "Your password has been changed succesfully"
    response = test_client.post(
        "/edit_password",
        data={
            "edit_current_password": "hardcoded_password",
            "edit_new_password": "new_password",
            "edit_new_password_confirm": "new_password"
        }
    )
    assert response.location.endswith("/profile")

    with test_client.session_transaction() as session:
        assert "change_password_success" in dict(session["_flashes"]).keys()
        assert dict(session["_flashes"])["change_password_success"] is not None
        assert dict(session["_flashes"])[
            "change_password_success"] == expected_flash
