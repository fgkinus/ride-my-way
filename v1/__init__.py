from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import APP_CONFIG

# initialize sql-alchemy
db = SQLAlchemy()


def register_blueprints(app):
    """Register the different blueprints with the application"""
    from .users import users_blueprint
    from .rides import rides_blueprint

    app.register_blueprint(users_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(rides_blueprint, url_prefix='/api/v1')


def create_app(config_name):
    """The application factory function"""

    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app
