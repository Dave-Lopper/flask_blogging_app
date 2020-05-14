# test/functional/test_user_logout.py
from app.models import User


def test_user_logs_out(test_client, db_init, insert_user):
    user = User.query.first()
    test_client.post(
        "/login",
        data={
            "login_email": user.email,
            "login_password": "hardcoded_password"
        }
    )
    with test_client.session_transaction():
        response = test_client.get("/logout")
        assert response.status_code == 302
        assert response.location.endswith("/")
        with test_client.session_transaction() as updated_session:
            assert "_user_id" not in updated_session
