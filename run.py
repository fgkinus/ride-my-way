from __future__ import absolute_import
from flask_jwt_extended import JWTManager
from flask_restplus import Api
import os

from app.utils import create_app, init_db, connect_db, register_namespace

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)  # create the Flask Instance
# api instance is instantiated
api = Api(
    app, version='1.0',
    title='RideMyWay API',
    description="The API to v1-My-Way ride sharing platform.",
)

init_db(db_name=app.config['DATABASE_NAME'], password=app.config['DATABASE_PASSWORD'],
        username=app.config['DATABASE_USER'])
DB = connect_db(db_name=app.config['DATABASE_NAME'], password=app.config['DATABASE_PASSWORD'],
                user=app.config['DATABASE_USER'])

app.config['DATABASE_CONN'] = DB

# register blueprints
# register_blueprints(app=app)
register_namespace(api)
# configure JWT
app.config['JWT_SECRET_KEY'] = app.config['SECRET']
# app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run()
