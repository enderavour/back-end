from app.models.user import User


def test_user_model():
    user = User(email="test@example.com", username="testuser", password="secret")
    assert user.email == "test@example.com"
    assert user.username == "testuser"
