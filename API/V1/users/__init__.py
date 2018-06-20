"""
The users Blueprint handles the user management for this application.
Specifically, this Blueprint allows for new users to register and for
users to log in and to log out of the application.
"""
from flask import Blueprint
from flask_restplus import Api

# Declare the blueprint
users_blueprint = Blueprint('users', __name__)

# Set up  the API and init the blueprint
api = Api()
api.init_app(users_blueprint)


# Set the default route
@users_blueprint.route('/')
def show():
    return {
        'message': 'authentication Endpoint'
    }
