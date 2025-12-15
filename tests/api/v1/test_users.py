from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from chatbot_gsantana.models.user import User


def test_create_user(client: TestClient, db_session: Session):
    """
    Test creating a new user.
    """
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword123",
    }
    # Assuming you have a user creation endpoint like this
    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201, f"Unexpected status code: {response.json()}"
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data  # Ensure password is not returned

    # Verify user is in the database
    user_in_db = (
        db_session.query(User).filter(User.username == user_data["username"]).first()
    )
    assert user_in_db is not None
    assert user_in_db.email == user_data["email"]


def test_login_for_access_token(client: TestClient, admin_user: User):
    """
    Test user login and token generation.
    This is explicitly testing the login endpoint.
    """
    login_data = {"username": admin_user.username, "password": "testpassword"}
    response = client.post("/api/v1/auth/token", data=login_data)

    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_read_current_user(client: TestClient, admin_auth_headers: dict):
    """
    Test accessing a protected endpoint to get the current user's data.
    """
    # Assuming you have a protected endpoint to get the current user
    response = client.get("/api/v1/users/me", headers=admin_auth_headers)

    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "admin_user"
    assert user_data["email"] == "admin@test.com"


def test_read_current_user_unauthenticated(client: TestClient):
    """
    Test that accessing a protected endpoint without authentication fails.
    """
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401  # Unauthorized
    assert response.json() == {"detail": "Not authenticated"}
