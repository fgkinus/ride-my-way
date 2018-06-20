from flask import Flask
import os

from instance.config import APP_CONFIG


def register_blueprints(app):
    """Register the different blueprints with the application"""
    pass


def create_app(config_name):
    """The application factory function"""

    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile(os.getcwd() + "\\instance\\config.py")

    return app
