from flask import Flask
import os
from config import APP_CONFIG, basedir
import psycopg2
from psycopg2.extras import RealDictCursor


def connect_db(db_name, user, password):
    try:
        conn = psycopg2.connect(database=db_name, user=user, password=password)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cursor
    except Exception:
        raise psycopg2.DatabaseError


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
    app.config.from_pyfile(os.path.join(basedir, 'config.py'))
    return app
