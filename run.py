from __future__ import absolute_import
from flask_jwt_extended import JWTManager
from flask_restplus import Api
import os

from app.utils import create_app, register_namespace
from db.utils import Database

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)  # create the Flask Instance
# api instance is instantiated
api = Api(
    app, version='2.0',
    title='RideMyWay API',
    description="The API to v1-My-Way ride sharing platform.",
)
# # database initialisation
# init_db(db_name=app.config['DATABASE_NAME'], password=app.config['DATABASE_PASSWORD'],
#         username=app.config['DATABASE_USER'])
# # connect to database
# DB = connect_db(db_name=app.config['DATABASE_NAME'], password=app.config['DATABASE_PASSWORD'],
#                 user=app.config['DATABASE_USER'])

Database = Database(username=app.config['DATABASE_USER'], password=app.config['DATABASE_PASSWORD'],
                    db_name=app.config['DATABASE_NAME']).init_db()

app.config['DATABASE_CONN'] = Database

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
