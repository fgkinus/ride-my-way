from __future__ import absolute_import
from flask_jwt_extended import JWTManager
from flask_restplus import Api
import os

from app import create_app, register_namespace

config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)  # create the Flask Instance
# api instance is instantiated
api = Api(
    app, version='2.0',
    title='RideMyWay API')

register_namespace(api)
# configure JWT
app.config['JWT_SECRET_KEY'] = app.config['SECRET']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run()
