# app.py
from flask import Flask
from extensions import db, bcrypt
from routes import init_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key_here'  # Replace with a strong random key in production

    # Configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmeazy.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Register Blueprints
    init_routes(app)

    return app
