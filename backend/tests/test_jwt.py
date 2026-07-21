from app.utils.jwt import create_access_token, decode_access_token


def test_create_and_decode_access_token():
    token = create_access_token("analyst@example.com")

    assert isinstance(token, str)
    assert len(token) > 0

    payload = decode_access_token(token)

    assert payload["sub"] == "analyst@example.com"
    assert "exp" in payload