"""
Initialize the rides Package and instantiate the API
"""
from flask import Blueprint, jsonify
from flask_restplus import Api

rides_blueprint = Blueprint('rides', __name__)

# Set up  the API and init the blueprint
api = Api(version='1.0', title='Rides EndPoint', description='Modify and interact with the Rides endpoints')
api.init_app(rides_blueprint)


# Set the default route
@rides_blueprint.route('/')
def show():
    return jsonify({
        'message': 'The rides endpoint'
    })
