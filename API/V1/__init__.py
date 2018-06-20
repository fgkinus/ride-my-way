from flask import Flask
import os

from instance.config import APP_CONFIG


def register_blueprints(app):
    """Register the different blueprints with the application"""
    from .users import users_blueprint
    from .rides import rides_blueprint

    app.register_blueprint(users_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(rides_blueprint, url_prefix='/api/v1')


def create_app(config_name):
    """The application factory function"""

    app = Flask(__name__)
    app.config.from_object(APP_CONFIG['development'])
    app.config.from_pyfile(os.getcwd() + "\\instance\\config.py")

    return app
