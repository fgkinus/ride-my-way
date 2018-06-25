"""
The users Blueprint handles the user management for this application.
Specifically, this Blueprint allows for new users to register and for
users to log in and to log out of the application.
"""
from flask import Blueprint, jsonify
from flask_restplus import Api


from v1.users import models
from . import Resources as resources

# Declare the blueprint
users_blueprint = Blueprint('users', __name__)

# Set up  the API and init the blueprint
api = Api()
api.init_app(users_blueprint)


# Set the default route
@users_blueprint.route('/')
def show():
    return jsonify(
        {
            'message': models.user_data
        }
    )


# Users endpoints
api.add_resource(resources.UserList, '/users')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogout, '/logout')
api.add_resource(resources.TokenRefresh, '/refresh')
api.add_resource(resources.UserRegistration, '/register')
