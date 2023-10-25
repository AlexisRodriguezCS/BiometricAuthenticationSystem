"""
user.py - User Model

This module defines the User model for representing registered users in the application.
"""

from database.db import db
from datetime import datetime
import pickle


class User(db.Model):
    """
    User class to represent registered users.

    Attributes:
        id (int): The user's unique identifier.
        username (str): The user's username.
        email (str): The user's email address.
        password (str): The hashed password of the user.
        salt (str): A unique salt used for password hashing.
        user_id (str): The unique user ID.
        created_date (datetime): The date and time of user account creation.
        biometric_data (bytes): Binary data for storing biometric information.

    Methods:
        __repr__(): Return a string representation of the User instance.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    salt = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.String(36), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    biometric_data = db.Column(db.PickleType)

    def __repr__(self):
        """
        Return a string representation of the User instance.

        :return: A string in the format "User(id=<id>, username='<username>', email='<email>')".
        """
        return f"User(id={self.id}, username='{self.username}', email='{self.email}')"
