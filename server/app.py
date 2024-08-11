"""
app.py - Flask Application Configuration

This module configures the Flask application, initializes extensions, and sets up routes.

Attributes:
    app: The Flask application instance.
    db: The SQLAlchemy object for database management.
    jwt: The JWTManager for managing JSON Web Tokens.
    limiter: The Limiter for rate limiting requests.
    migrate: The Migrate object for database migrations.

"""
from flask import Flask
from config import app_config
from database.db import db
from routes.user import user_bp
from flask_migrate import Migrate
from flask_limiter import Limiter
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS

load_dotenv()


def create_app(config_name=None):
    """
    Create a Flask application instance with the specified configuration.

    :param config_name: The name of the configuration to use. Defaults to "development" if not provided.
    :return: A Flask application instance.
    """
    app = Flask(__name__)

    # Enable CORS for all domains on all routes
    CORS(app)

    # Enable CORS with specific origin(s)
    CORS(app, resources={
         r"/user/*": {"origins": "https://biometricauthenticationsystem.netlify.app"}})

    # Load the default configuration if config_name is not provided
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    # Use the specified configuration from app_config or default to "development"
    app.config.from_object(app_config.get(
        config_name, app_config["development"]))

    # Create an instance of JWTManager and configure it
    jwt = JWTManager(app)

    # Configure JWT settings here
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    # Specify the path to the certificate and key files
    # cert_file = os.path.join(os.path.dirname(__file__), 'cert.pem')
    # key_file = os.path.join(os.path.dirname(__file__), 'key.pem')

    # Configure the SSL context
    # app.config['SSL_CONTEXT'] = (cert_file, key_file)

    db.init_app(app)  # Initialize Flask-SQLAlchemy

    # Initialize Flask-Limiter after creating the app
    limiter = Limiter(
        app,
        default_limits=["5 per minute"],  # Set the default rate limit here
    )

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix="/user")

    @app.route('/')
    def index():
        return 'Welcome to Biometric App Server', 200

    return app


# Create the Flask app
app = create_app("production")

# Initialize Flask-Migrate
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Run the app with SSL context
    # app.run(ssl_context=("cert.pem", "key.pem"))
    app.run()
