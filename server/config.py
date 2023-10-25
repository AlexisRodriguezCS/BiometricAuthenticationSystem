# config.py
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


class Config:
    """Base configuration class."""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add this configuration option to force HTTPS
    # SESSION_COOKIE_SECURE = True


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    # Secret key for session management
    JWT_SECRET_KEY = os.getenv("DEV_SECRET_KEY")


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # PostgreSQL database URL for testing
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL")
    # Secret key for session management
    JWT_SECRET_KEY = os.getenv("TEST_SECRET_KEY")


class ProductionConfig(Config):
    """Production configuration."""
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")
    # Secret key for session management
    JWT_SECRET_KEY = os.getenv("PROD_SECRET_KEY")


# Define a dictionary to map configuration names to their respective classes
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
