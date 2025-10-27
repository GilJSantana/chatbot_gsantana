from datetime import timedelta

from jose import jwt

from chatbot_gsantana.core import security
from chatbot_gsantana.core.config import get_settings


def test_password_hashing():
    password = "testpassword"
    hashed_password = security.get_password_hash(password)
    assert hashed_password != password
    assert security.verify_password(password, hashed_password)
    assert not security.verify_password("wrongpassword", hashed_password)


def test_create_access_token():
    settings = get_settings()
    data = {"sub": "testuser"}
    expires_delta = timedelta(minutes=15)
    token = security.create_access_token(data, expires_delta=expires_delta)

    decoded_payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded_payload["sub"] == "testuser"
    assert "exp" in decoded_payload
