"""
db.py - Database Configuration

This module configures the database using Flask-SQLAlchemy.

Attributes:
    db (SQLAlchemy): The SQLAlchemy object for database management.

"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
