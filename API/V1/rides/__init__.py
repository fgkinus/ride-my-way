"""
Initialize the rides Package and instantiate the API
"""
from flask import Blueprint, jsonify
from flask_restplus import Api

from V1.rides import Resources

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


# add list rides view
api.add_resource(Resources.ListRideOffers, '/rides')
api.add_resource(Resources.GetRideOffer, '/rides/<int:offer_id>')  # display specific ride
# add ride offer
api.add_resource(Resources.AddRideOffer, '/rides')

# Requests Views
api.add_resource(Resources.GetRideRequests, '/rides/<int:offer_id>/requests')  # get ride requests by ride id
api.add_resource(Resources.AddRideRequest, '/rides/<int:offer_id>/requests')  # add ride request by ride_request id
api.add_resource(Resources.ListRideRequests, '/ride-requests')  # get ride request list
