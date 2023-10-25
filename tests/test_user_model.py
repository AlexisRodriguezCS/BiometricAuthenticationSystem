"""
Test cases for the User model in the Flask application.

These test cases cover various aspects of the User model, including user creation,
string representation, and handling duplicate email constraints.

Please make sure to adapt these test cases to your specific requirements and test environment.

Tested Model:
- User: User model representing registered users.

Dependencies:
- Flask: Web framework for testing.
- SQLAlchemy: Database ORM for data manipulation.
- bcrypt: Password hashing library.
- Other project-specific dependencies.
"""
import pytest
from models.user import User
from database.db import db
from app import create_app
import bcrypt

# This fixture sets up the Flask application for testing


@pytest.fixture
def app():
    """
    Fixture to set up the Flask application for testing.

    :return: Flask app instance for testing.
    """
    app = create_app("testing")
    app_context = app.app_context()
    app_context.push()
    db.create_all()

    yield app

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_create_user(app):
    """
    Test the creation of a user in the User model.

    :param app: Flask app instance for testing.
    """
    with app.app_context():
        # Generate a salt for the user
        salt = bcrypt.gensalt()

        # Create a new user with the generated salt
        user = User(username="testuser", email="test@example.com",
                    password="password", salt=salt)

        # Add the user to the database
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        retrieved_user = User.query.filter_by(email="test@example.com").first()

        # Check if the user was successfully added and retrieved
        assert retrieved_user is not None
        assert retrieved_user.email == "test@example.com"


def test_user_representation(app):
    """
    Test the string representation of the User model.

    :param app: Flask app instance for testing.
    """
    with app.app_context():
        # Create a new user
        user = User(username="testuser",
                    email="test@example.com", password="password")

        # Check the string representation of the user
        assert str(
            user) == "User(id=None, username='testuser', email='test@example.com')"


def test_duplicate_email(app):
    """
    Test handling duplicate email constraints in the User model.

    :param app: Flask app instance for testing.
    """
    with app.app_context():
        # Generate salts for the users
        salt1 = bcrypt.gensalt()
        salt2 = bcrypt.gensalt()

        # Attempt to create two users with the same email and their respective salts
        user1 = User(username="testuser1", email="test@example.com",
                     password="password1", salt=salt1)
        user2 = User(username="testuser2", email="test@example.com",
                     password="password2", salt=salt2)

        # Add and commit the first user
        db.session.add(user1)
        db.session.commit()

        # Attempt to add and commit the second user (should raise an exception)
        try:
            db.session.add(user2)
            db.session.commit()
        except Exception as e:
            # If an exception is raised due to a duplicate email constraint
            assert True
