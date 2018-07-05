from __future__ import absolute_import
from flask import Flask
import os

from config import APP_CONFIG, basedir
import psycopg2
from psycopg2.extras import RealDictCursor

from db.queries import tables_list
from db.utils import check_db_exists, create_db, create_tables


def connect_db(db_name, user, password):
    try:
        conn = psycopg2.connect(database=db_name, user=user, password=password)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        return conn, cursor
    except Exception:
        raise psycopg2.DatabaseError


def init_db(db_name, username='postgres', password=''):
    try:
        conn = psycopg2.connect(database='postgres', user=username, password=password)
    except psycopg2.DatabaseError:
        raise psycopg2.DatabaseError("could not initiate database connection")
    if check_db_exists(conn=conn, db_name=db_name)[0]['exists']:
        pass
    else:
        create_db(conn, db_name)
        conn = connect_db(db_name=db_name, user='postgres', password=os.getenv('DATABASE_PASSWORD'))
        create_tables(conn[0], tables_list)


def register_blueprints(app):
    """Register the different blueprints with the application"""

    from app.users import users_blueprint
    from app.rides import rides_blueprint
    app.register_blueprint(users_blueprint, url_prefix='/api/v1/auth')
    app.register_blueprint(rides_blueprint, url_prefix='/api/v1')


def register_namespace(root):
    """
    add namespaces to endpoints
    :param root:
    :return:
    """
    from app.rides import api as rides_ns
    from app.users import api as users_ns
    root.add_namespace(rides_ns, path='/api/v1')
    root.add_namespace(users_ns, path='/api/v1/auth')


def create_app(config_name):
    """The application factory function"""

    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile(os.path.join(basedir, 'config.py'))
    return app
