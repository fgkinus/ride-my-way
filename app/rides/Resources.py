from __future__ import absolute_import
import datetime
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError, WrongTokenError
from flask_restplus import Resource, reqparse, Namespace

# define a namespace for rides
from jwt import ExpiredSignature

from app.rides.models import Ride

api = Namespace('rides', description='rides related operations')


# error handlers
@api.errorhandler(NoAuthorizationError)
def handle_no_auth_exception(error):
    """Handle ethe jwt required exception when none s provided"""
    return {'message': 'No authentication token provided'}, 401


@api.errorhandler(ExpiredSignature)
def handle_expired_token(error):
    return {'message': 'authentication token provided is expired'}, 401


@api.errorhandler(WrongTokenError)
def handle_expired_token(error):
    return {'message': 'Provide a refresh token rather than an access token'}, 401


@api.route('/rides', endpoint='list-rides')
@api.doc('list rides')
class RideOffers(Resource):
    """A view to list all ride offers and individual rides"""
    # define  request parsers and args
    ride_parser = reqparse.RequestParser()
    ride_parser.add_argument('id', help='This field can be blank', required=False)
    ride_parser.add_argument('driver', help='This field cannot be blank', required=False)
    ride_parser.add_argument('origin', help='This field cannot be blank', required=True)
    ride_parser.add_argument('destination', help='This field cannot be blank', required=True)
    ride_parser.add_argument('departure_time', help='This field cannot be blank', required=True)
    ride_parser.add_argument('vehicle_model', help='This field cannot be blank', required=True)
    ride_parser.add_argument('vehicle_capacity', help='This field cannot be blank', required=True)
    ride_parser.add_argument('route', help='This field cannot be blank', required=False)
    ride_parser.add_argument('time_added', help='This field cannot be blank', required=False)

    @jwt_required
    def get(self):
        """List all ride offers"""
        ride = Ride()
        try:
            ride_offers = ride.list_all_rides()
            return jsonify({'ride-offers': ride_offers})
        except:
            return {
                       'message': ' Error getting rides list'
                   }, 500

    @jwt_required
    @api.expect(ride_parser)
    def post(self):
        """add a new ride offer"""
        data = self.ride_parser.parse_args()
        # set the driver to current logged in user
        data['driver'] = get_jwt_identity()
        # verify user is a driver and can add rides
        ride = Ride(data=data)
        try:
            new_ride = ride.add_ride(get_jwt_identity())
            if new_ride is False:
                return {
                           "message": "Unauthorised operation",
                           "Details": "A passenger is not permitted to add trips"
                       }, 401
        except:
            return {
                       "error": "could not complete operation"
                   }, 500

            # a try catch to handle errors arising from query execution

        return {
                   'message': "new trip added",
                   'trip': new_ride,
               }, 201


@api.route('/rides/<offer_id>', endpoint='get-ride')
@api.doc('get a specific ride')
class GetRideOffer(Resource):
    """Get a specific ride offer by ride id"""

    @api.doc(params={'id': 'The ride Id'})
    @jwt_required
    def get(self, offer_id):
        """Fetch a specific ride"""
        ride = Ride()
        try:
            ride_offer = ride.get_ride(offer_id)
            return jsonify(
                {
                    'ride-offers': ride_offer
                }
            )
        except:
            return {
                       'message': ' Error getting ride list'
                   }, 500

    @jwt_required
    @api.doc(params={'id': 'The ride offer id to delete'})
    def delete(self, offer_id):
        """
        delete a ride offer if you are the owner
        :param offer_id:
        :return:
        """
        ride = Ride().delete_ride(ride_id=offer_id, current_user=get_jwt_identity())
        # ensure a ride request exists
        if ride[1] == 1:
            return {
                       "message": "Trip offer not Found"
                   }, 204
        elif ride[1] == 2:
            return {
                       'message': " sorry {} You are not authorised to remove this ride".format(get_jwt_identity())
                   }, 401

        return {
                   'message': 'Record successfully deleted',
                   'ride': ride
               }, 200


@api.route('/rides/<offer_id>/requests', endpoint='offer-ride-requests')
@api.doc('get a specific ride', params={'offer_id': 'An ID for ride offer'})
class RideRequests(Resource):
    @jwt_required
    def get(self, offer_id):
        """
        get a list of ride requests made for a specific ride
        :param offer_id:
        :return request, ride:
        """
        ride = Ride()
        try:
            ride_offer = ride.get_ride_request(ride_id=offer_id)
        except:
            return jsonify(
                {
                    'message': ' Error getting ride '
                }
            ), 500
        # ensure a ride request exists
        if ride_offer is False:
            return {
                       "message": "Trip offer not Found"
                   }, 204
        try:
            return jsonify(
                {
                    "requests": ride_offer[0],
                    'ride-details': ride_offer[1]
                }
            )
        except:
            return {
                       "message": "could not fetch ride requests"
                   }, 500

    @jwt_required
    def post(self, offer_id):
        """add a new ride request"""

        username = get_jwt_identity()
        ride = Ride()
        ride_request = ride.add_ride_request(ride_id=offer_id, username=username)

        if ride_request is False:
            return {
                       "message": "ride offer not found"
                   }, 204

        return make_response(
            jsonify(
                {
                    "message": "Trip request added",
                    "request": ride_request
                }
            ), 201
        )


@api.route('/rides/<req_id>/requests', endpoint='remove-ride-requests')
@api.doc('remove a specific ride', params={'req_id': 'An ID for ride request'})
class RemoveRequests(Resource):
    @jwt_required
    def delete(self, req_id):
        """delete a ride request if you own the ride"""
        request = Ride().remove_ride_request(req_id, get_jwt_identity())
        if len(request) != 1:
            return {
                       'message': 'ride not deleted',
                       'details': 'ride does not exist or you are not authorised to delete it'
                   }, 200
        else:
            return {
                       "message": "trip request deleted"
                   }, 201


@api.route('/rides/requests', endpoint='all-ride-requests')
class ListRideRequests(Resource):
    """A view to list all ride requests """

    @jwt_required
    def get(self):
        """List all ride requests"""
        ride = Ride()

        requests = ride.list_ride_request()
        return jsonify(
            {
                "requests": requests
            }
        )


@api.route('/rides/<req_id>/<response>', endpoint='make-ride-response')
@api.doc('respond to a specific ride',
         params={'req_id': 'An ID for ride offer', 'response': 'a response to the request'})
class RespondToRequest(Resource):
    """ Add responses to ride requests for drivers"""

    @jwt_required
    def post(self, req_id, response):
        """ride owners add  ride responses"""
        # validate response is valid
        responses = ('accept', 'reject',)
        if response not in responses:
            return {
                       'message': 'Invalid Response'
                   }, 400
        ride = Ride()
        try:
            added_response = ride.respond_to_request(req_id, response, get_jwt_identity())
        except:
            return {
                       "message": "Error adding response",
                       "details": "Check that response is valid ie {} or {}".format('Reject', 'Accept'),
                       "more-details": "If response has previously been made the operation will fail too"
                   }, 400
        # verify request exists
        if added_response[0] is False and added_response[1] == 1:
            return {}, 204
        # verify current user owns the trip and can accept request
        if added_response[0] is False and added_response[1] == 2:
            return {"message": "Unauthorised operation.You don't own the request"}, 401
        # Add response to DB
        return jsonify(
            {
                'message': 'Response recorded',
                'response': added_response
            }
        )


@api.route('/rides/<req_id>/response', endpoint='get-ride-response')
@api.doc('get a specific ride request response', params={'req_id': 'An ID for ride request'})
class GetRequestResponse(Resource):
    """ a resource to handle urls for request responses"""

    @jwt_required
    def get(self, req_id):
        """get response for rides if you are the requester or owner of ride"""
        ride = Ride()
        try:
            response = ride.get_req_response(req_id)
        except:
            return {'error': "couldn't fetch response to request"}, 400
        # verify responses are present
        if len(response) != 1:
            return {'message': 'no response found for ride request id {}'.format(req_id)}, 200
        # if current user is not the requester or the driver  they cannot view the ride response
        elif response[0]['username'] != get_jwt_identity() or response[0]['driver'] != get_jwt_identity():
            return {
                       'message': " You are not authorised to view that ride response"
                   }, 401
        # return response to request
        return jsonify({'response': response})
