"""
Test cases for user-related routes in the Flask application.

These test cases cover various user-related functionality, including registration, login,
token refresh, biometric data storage, and more. They ensure that the user routes are
working as expected and handle various scenarios, including authentication, registration,
and data storage.

Please make sure to adapt these test cases to your specific requirements and test environment.

Tested Routes:
- /user/details
- /user/refresh_token
- /user/register
- /user/login
- /user/delete_account
- /user/store_biometric_data
- /user/authenticate_with_biometrics

Dependencies:
- Flask: Web framework for testing.
- Flask-JWT-Extended: JWT authentication extension for Flask.
- SQLAlchemy: Database ORM for data manipulation.
- Other project-specific dependencies.

"""

import pytest
from app import create_app
from database.db import db
from models.user import User
from routes.user import user_bp


@pytest.fixture
def app():
    """
    Fixture to set up the Flask application for testing.

    :return: Flask app instance for testing.
    """
    app = create_app("testing")
    app.register_blueprint(user_bp)
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_get_user_details(app, jwt_token):
    """
    Test the route to get user details.

    :param app: Flask app instance for testing.
    :param jwt_token: JWT token for authentication.
    """
    with app.app_context():
        # Create a test user
        user = User(username="testuser",
                    email="test@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Get the user's details with a valid JWT token
        response = app.test_client().get(
            "/user/details", headers={"Authorization": f"Bearer {jwt_token}"}
        )

        assert response.status_code == 200

        data = response.get_json()
        assert data["message"] == "success"
        assert data["user"]["username"] == "testuser"
        assert data["user"]["email"] == "test@example.com"


def test_refresh_token(app, jwt_token, refresh_token):
    """
    Test the route to refresh a JWT token.

    :param app: Flask app instance for testing.
    :param jwt_token: JWT token for authentication.
    :param refresh_token: Refresh token for token refresh.
    """
    with app.app_context():
        # Send a POST request to refresh the JWT token
        response = app.test_client().post(
            "/user/refresh_token",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={"refresh_token": refresh_token},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["message"] == "Token refreshed successfully"
        assert "access_token" in data


def test_register_user(app):
    """
    Test the route to register a user.

    :param app: Flask app instance for testing.
    """
    # Create a test client
    client = app.test_client()

    # Send a POST request to register a user
    response = client.post(
        "/user/register", json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Registration successful"
    assert "access_token" in data
    assert "refresh_token" in data


def test_register_duplicate_email(app):
    """
    Test the route to register a user with a duplicate email.

    :param app: Flask app instance for testing.
    """
    # Create a test client
    client = app.test_client()

    # Register a user with the same email twice
    client.post(
        "/user/register", json={"username": "testuser", "email": "test@example.com", "password": "password1"}
    )
    response = client.post(
        "/user/register", json={"username": "testuser", "email": "test@example.com", "password": "password2"}
    )

    assert response.status_code == 400


def test_login_user(app):
    """
    Test the route to log in a user.

    :param app: Flask app instance for testing.
    """
    # Create a test client
    client = app.test_client()

    # Register a user
    client.post(
        "/user/register", json={"username": "testuser", "email": "test@example.com", "password": "password"}
    )

    # Send a POST request to log in the user
    response = client.post(
        "/user/login", json={"usernameEmail": "testuser", "password": "password"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful"
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_invalid_credentials(app):
    """
    Test the route to log in with invalid credentials.

    :param app: Flask app instance for testing.
    """
    # Create a test client
    client = app.test_client()

    # Send a POST request to log in with invalid credentials
    response = client.post(
        "/user/login", json={"usernameEmail": "testuser", "password": "wrongpassword"}
    )

    assert response.status_code == 401


def test_delete_account(app, jwt_token):
    """
    Test the route to delete a user account.

    :param app: Flask app instance for testing.
    :param jwt_token: JWT token for authentication.
    """
    with app.app_context():
        # Create a test user
        user = User(username="testuser",
                    email="test@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Send a DELETE request to delete the user account with a valid JWT token
        response = app.test_client().delete(
            "/user/delete_account",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={"email": "test@example.com", "password": "password"},
        )

        assert response.status_code == 200

        # Check if the user account was deleted from the database
        user = User.query.filter_by(email="test@example.com").first()
        assert user is None


def test_store_biometric_data(app, jwt_token):
    """
    Test the route to store biometric data for a user.

    :param app: Flask app instance for testing.
    :param jwt_token: JWT token for authentication.
    """
    with app.app_context():
        # Create a test user
        user = User(username="testuser",
                    email="test@example.com", password="password")
        db.session.add(user)
        db.session.commit()

        # Send a POST request to store biometric data with a valid JWT token
        response = app.test_client().post(
            "/user/store_biometric_data",
            headers={"Authorization": f"Bearer {jwt_token}"},
            json={"faceData": "base64_encoded_data"},
        )

        assert response.status_code == 200

        # Check if biometric data is stored in the user's record
        user = User.query.filter_by(email="test@example.com").first()
        assert user.biometric_data == "base64_encoded_data"


def test_authenticate_with_biometrics(app):
    """
    Test the route to authenticate with biometric data.

    :param app: Flask app instance for testing.
    """
    with app.app_context():
        # Create a test user with stored biometric data
        user = User(username="testuser",
                    email="test@example.com", password="password")
        user.biometric_data = "base64_encoded_data"
        db.session.add(user)
        db.session.commit()

        # Send a POST request to authenticate with biometrics
        response = app.test_client().post(
            "/user/authenticate_with_biometrics",
            json={"faceData": "base64_encoded_data"},
        )

        assert response.status_code == 200

        data = response.get_json()
        assert data["message"] == "Biometric authentication successful"
        assert "access_token" in data
        assert "refresh_token" in data
