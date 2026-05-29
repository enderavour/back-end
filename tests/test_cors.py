from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_cors_headers():
    response = client.options(
        "/",
        headers={
            "Origin": "http://example.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
