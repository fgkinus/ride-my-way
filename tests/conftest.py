import pytest
import sys, os
import run
from app.utils import Database as db
from flask_jwt_extended import JWTManager

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from flask_restplus import Api
from app import utils
from db.utils import Database


@pytest.fixture
def test_client():
    app = run.create_app('testing')  # create app instance with testing context
    dbname = app.config['DATABASE_NAME']  # get the database name for testing
    username = app.config['DATABASE_USER']
    password = app.config['DATABASE_PASSWORD']
    api = Api(app)  # initialise api instance
    db = Database(db_name=dbname, username=username,
                  password=password).init_db()  # initialize db iff missing
    run.register_namespace(api)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    # configure JWT
    app.config['JWT_SECRET_KEY'] = app.config['SECRET']
    jwt = JWTManager(app)
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def test_db():
    dbname = os.getenv('TESTING_DB_NAME')  # get the database name for testing
    username = os.getenv('TESTING_DB_USER')
    password = os.getenv('TESTING_DB_PASSWORD')
    db = Database(username=username, password=password, db_name=dbname)
    yield db
