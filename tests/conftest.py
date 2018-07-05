import pytest
import sys, os
from flask_jwt_extended import JWTManager

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from flask_restplus import Api
from app import utils


@pytest.fixture
def test_client():
    app = utils.create_app('testing')  # create app instance with testing context
    dbname = app.config['DATABASE_NAME']  # get the database name for testing
    username = app.config['DATABASE_USER']
    password = app.config['DATABASE_PASSWORD']
    api = Api(app)  # initialise api instance
    utils.init_db(db_name=dbname, username=username, password=password)  # initialize db iff missing
    utils.register_namespace(api)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # configure JWT
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    jwt = JWTManager(app)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()
