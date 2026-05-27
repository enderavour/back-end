from app.models.user import User


def test_user_has_timestamps():
    user = User()

    assert hasattr(user, "created_at")
    assert hasattr(user, "updated_at")
