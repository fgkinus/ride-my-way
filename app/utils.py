from __future__ import absolute_import
from flask import Flask
import os

from config import APP_CONFIG, basedir


def register_namespace(root):
    """
    add namespaces to endpoints
    :param root:
    :return:
    """
    from app.rides.Resources import api as rides_ns
    from app.users.Resources import api as users_ns
    root.add_namespace(rides_ns, path='/api/v2')
    root.add_namespace(users_ns, path='/api/v2/auth')


def create_app(config_name):
    """The application factory function"""

    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])
    app.config.from_pyfile(os.path.join(basedir, 'config.py'))
    return app
