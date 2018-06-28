import json
import os
import tempfile
from json import JSONDecodeError

import pytest
from flask_jwt_extended import create_access_token, JWTManager

from v1 import create_app, register_blueprints, connect_db


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


@pytest.fixture
def test_client():
    app = create_app('testing')
    register_blueprints(app=app)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # configure JWT
    app.config[
        'JWT_SECRET_KEY'] = '$pbkdf2-sha256$29000$I.T8f8/ZG8M4J0QIwTgHIA$.9wCvRZECxd7/yvHttEgoHzpvgjdhjizq5ySewKfeQc'
    jwt = JWTManager(app)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


