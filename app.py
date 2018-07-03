from __future__ import absolute_import
from flask_jwt_extended import JWTManager
from flask_restplus import Api
import os

from v1 import create_app, register_blueprints, init_db, connect_db

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)  # create the Flask Instance
# api instance is instantiated
api = Api(
    app, version='1.0',
    title='RideMyWay API',
    description="The API to v1-My-Way ride sharing platform. To see sample login credentials navigate to '/api/vi/auth'",
)

init_db(db_name=app.config['DATABASE_NAME'])
DB = connect_db(db_name=app.config['DATABASE_NAME'], password=app.config['DATABASE_PASSWORD'],
                user=app.config['DATABASE_USER'])

app.config['DATABASE_CONN'] = DB

# register blueprints
register_blueprints(app=app)

# configure JWT
app.config['JWT_SECRET_KEY'] = '$pbkdf2-sha256$29000$I.T8f8/ZG8M4J0QIwTgHIA$.9wCvRZECxd7/yvHttEgoHzpvgjdhjizq5ySewKfeQc'
# app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

if __name__ == '__main__':
    print(os.getenv('DATABASE_PASSWORD'))
    app.run()
