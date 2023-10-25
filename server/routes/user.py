# routes/user.py - User Routes
"""
Routes for user-related functionality in the Flask application.

These routes provide functionality for user registration, authentication, token refresh,
biometric data storage, and more. Ensure to adapt these routes to your specific requirements
and use them in your project.

Implemented Routes:
- /user/details: Retrieve user details.
- /user/refresh_token: Refresh an access token.
- /user/register: User registration.
- /user/login: User login.
- /user/logout: User logout.
- /user/delete_account: Delete user account.
- /user/store_biometric_data: Store biometric data.
- /user/authenticate_with_biometrics: Authenticate with biometric data.

Dependencies:
- Flask: Web framework for routing and request handling.
- Flask-JWT-Extended: JWT authentication extension for Flask.
- SQLAlchemy: Database ORM for data manipulation.
- bcrypt: Password hashing library.
- Other project-specific dependencies.
"""

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify, current_app
from models.user import User
from database.db import db
from validate_email_address import validate_email
import bcrypt
import jwt  # Import JWT library
import datetime
import uuid  # Import uuid library
from sqlalchemy import or_  # Import the 'or_' function
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
import base64  # For encoding/decoding binary data

user_bp = Blueprint("user", __name__)


@user_bp.route("/details", methods=["GET"])
@jwt_required()  # Requires a valid JWT token
def get_user_details():
    """
    Retrieve user details using a valid JWT token.

    :return: User details in JSON format.
    """
    try:
        # Get the user ID from the token
        current_user_id = get_jwt_identity()

        # Retrieve user details using the user ID
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            user_details = {
                "username": user.username,
                "email": user.email,
                "userId": user.user_id,
                "accountCreationDate": user.created_date.strftime("%m/%d/%Y"),
            }
            return jsonify({"message": "success", "user": user_details}), 200

        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "An error occurred"}), 500


@user_bp.route("/refresh_token", methods=["POST"])
@jwt_required(refresh=True)  # Requires a valid refresh token
def refresh_token():
    """
    Refresh the access token using a valid refresh token.

    :return: New access token in JSON format.
    """
    # Get the current user's identity from the valid refresh token
    current_user_id = get_jwt_identity()

    # Generate a new access token with a 60-minute expiration
    access_token = create_access_token(
        identity=current_user_id, expires_delta=datetime.timedelta(minutes=60))

    return jsonify({"message": "Token refreshed successfully", "access_token": access_token}), 200


@user_bp.route("/register", methods=["POST"])
def register():
    """
    Route for user registration.

    :return: Registration status and tokens in JSON format.
    """
    # Extract user data from request
    email = request.json.get("email")
    password = request.json.get("password")
    username = request.json.get("username")

    # Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Email is already registered"}), 400

    # Check if the username is already taken
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({"message": "Username is not available"}), 400

    # Check if the username is provided and not empty
    if not username:
        return jsonify({"message": "Username is required"}), 400

    # Check if the password is too short
    if len(password) < 8:
        return jsonify({"message": "Password is too short (minimum 8 characters)"}), 400

    # Check if the email is valid
    if not validate_email(email):
        return jsonify({"message": "Invalid email address"}), 400

    # Generate a unique 'user_id' for this user
    user_id = str(uuid.uuid4())  # Generate a UUID

    # Generate a unique salt for this user
    salt = bcrypt.gensalt()

    # Hash the password using bcrypt with the user's unique salt
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    new_user = User(username=username, email=email, password=hashed_password.decode(
        "utf-8"), salt=salt.decode("utf-8"), user_id=user_id)

    try:
        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Generate a JWT token with a 2 hour expiration
        access_token = create_access_token(
            identity=new_user.id, expires_delta=datetime.timedelta(hours=2))

        # Generate a refresh token with a longer expiration (e.g., 7 days)
        refresh_token = create_refresh_token(
            identity=new_user.id, expires_delta=datetime.timedelta(days=7))

        return jsonify({"message": "Registration successful", "access_token": access_token, "refresh_token": refresh_token}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500


@user_bp.route("/login", methods=["POST"])
def login():
    """
    Route for user login.

    :return: Login status and tokens in JSON format.
    """
    # Extract user data from request
    username_email = request.json.get("usernameEmail")  # Get email or username
    password = request.json.get("password")

    # Find the user by email or username
    user = User.query.filter(
        or_(User.email == username_email, User.username == username_email)).first()

    if user:

        # Check the password using bcrypt with the user's salt
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            # Generate an access token with a 2-hour expiration
            access_token = create_access_token(
                identity=user.id, expires_delta=datetime.timedelta(hours=2))

            # Generate a refresh token with a longer expiration (e.g., 7 days)
            refresh_token = create_refresh_token(
                identity=user.id, expires_delta=datetime.timedelta(days=7))

            return jsonify({"message": "Login successful", "access_token": access_token, "refresh_token": refresh_token}), 200

    return jsonify({"message": "Invalid email or username or password"}), 401


@user_bp.route("/logout", methods=["POST"])
def logout():
    """
    Route for user logout.

    :return: Logout status in JSON format.
    """
    # You can add additional security checks here if needed
    return jsonify({"message": "Logout successful"}), 200


@user_bp.route("/delete_account", methods=["DELETE"])
def delete_account():
    """
    Route for user account deletion.

    :return: Account deletion status in JSON format.
    """
    # Extract user data from request
    email = request.json.get("email")

    # Find the user by email
    user = User.query.filter_by(email=email).first()

    if user:
        try:
            # Delete the user's account from the database
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "Account deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Account deletion failed: {str(e)}"}), 500

    return jsonify({"message": "Invalid email or password"}), 401


@user_bp.route("/store_biometric_data", methods=["POST"])
# Authentication & Authorization: Ensure the request is from an authenticated user
@jwt_required()
def store_biometric_data():
    """
    Route to store biometric data for a user.

    :return: Biometric data storage status in JSON format.
    """
    try:
        # Authentication & Authorization: Identify the current user
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if user:
            face_data = request.json.get("faceData")

            if not face_data:
                # Request Validation: Ensure the received data is not empty or invalid
                return jsonify({"message": "Invalid or missing face data"}), 400

            try:
                # Data Sanitization: Verify and process the biometric data
                decoded_face_data = base64.b64decode(face_data)
                user.biometric_data = decoded_face_data
            except Exception as e:
                return jsonify({"message": "Invalid face data format"}), 400

            # Database Update: Store the sanitized biometric data in the user's record
            db.session.commit()

            return jsonify({"message": "Biometric data stored successfully"}), 200
        else:
            # User Not Found
            return jsonify({"message": "User not found"}, 404)
    except Exception as e:
        print("Error:", str(e))
        # Internal Server Error
        return jsonify({"error": "An error occurred while storing biometric data"}, 500)


@user_bp.route("/authenticate_with_biometrics", methods=["POST"])
def authenticate_with_biometrics():
    """
    Route to authenticate a user with biometric data.

    :return: Authentication status and tokens in JSON format.
    """
    try:
        # Retrieve and process the provided face data
        face_data = request.json.get("faceData")
        decoded_face_data = base64.b64decode(face_data)

        # Search for a user with matching biometric data
        user = User.query.filter_by(biometric_data=decoded_face_data).first()

        if user:
            # Generate access and refresh tokens
            access_token = create_access_token(
                identity=user.id, expires_delta=datetime.timedelta(hours=2))
            refresh_token = create_refresh_token(
                identity=user.id, expires_delta=datetime.timedelta(days=7))
            # Successful Authentication
            return jsonify({
                "message": "Biometric authentication successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200

        # Authentication Failed
        return jsonify({"message": "Biometric authentication failed"}, 401)
    except Exception as e:
        print("Error:", str(e))
        # Internal Server Error
        return jsonify({"error": "An error occurred during biometric authentication"}, 500)


@user_bp.route('/start-backend', methods=['GET'])
def start_backend():
    """
    Route to start the backend.

    This route allows the client to initiate the backend service upon making a POST request. The backend initialization can include setting up services, database connections, or other necessary components to start the application.

    :return: A success message in JSON format to indicate that the backend has been started.
    """
    return jsonify({"message": "Backend started successfully"}), 200
