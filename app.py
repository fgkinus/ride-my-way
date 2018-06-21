from flask_jwt_extended import JWTManager
from flask_restplus import Api
from jwt import exceptions as jwt_exceptions

from v1 import create_app, register_blueprints

app = create_app('development')  # create the Flask Instance
# simple error handling
errors = {
    'UserAlreadyExistsError': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'NoAuthorizationError': {
        'message': "Authentication header not provided",
        'status': 401,
        'extra': "Login to get JWT token.",
    },
    jwt_exceptions.ExpiredSignature: {
        'message': "JWT token expired",
        'status': 401,
        'extra': "Please Refresh",
    },
}
# api instance is instantiated
api = Api(
    app, version='1.0',
    title='RideMyWay API',
    description="The API to v1-My-Way ride sharing platform",
    errors=errors
)
# register blueprints
register_blueprints(app=app)

# configure JWT
app.config['JWT_SECRET_KEY'] = '$pbkdf2-sha256$29000$I.T8f8/ZG8M4J0QIwTgHIA$.9wCvRZECxd7/yvHttEgoHzpvgjdhjizq5ySewKfeQc'
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run()
