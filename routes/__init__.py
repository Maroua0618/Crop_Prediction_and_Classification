from flask import Blueprint

from .auth_routes import auth_bp
from .main_routes import main_bp
from .classification_routes import classification_bp
from .prediction_routes import prediction_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(classification_bp)
    app.register_blueprint(prediction_bp)