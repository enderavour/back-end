from app.schemas.user import SignUpRequest


def test_signup_schema():
    payload = SignUpRequest(
        email="test@example.com", username="tester", password="123456"
    )

    assert payload.email == "test@example.com"
    assert payload.username == "tester"
