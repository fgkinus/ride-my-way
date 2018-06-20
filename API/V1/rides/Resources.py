import time
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, reqparse

from V1.rides import models

# define  request parsers and args
ride_parser = reqparse.RequestParser()
ride_parser.add_argument('id', help='This field can be blank', required=False)
ride_parser.add_argument('driver', help='This field cannot be blank', required=True)
ride_parser.add_argument('origin', help='This field cannot be blank', required=True)
ride_parser.add_argument('destination', help='This field cannot be blank', required=True)
ride_parser.add_argument('departure_time', help='This field cannot be blank', required=True)
ride_parser.add_argument('vehicle_model', help='This field cannot be blank', required=True)
ride_parser.add_argument('vehicle_capacity', help='This field cannot be blank', required=True)
ride_parser.add_argument('route', help='This field cannot be blank', required=False)
ride_parser.add_argument('time_added', help='This field cannot be blank', required=False)

request_parser = reqparse.RequestParser()
request_parser.add_argument('id', help='This field can be blank', required=False)
request_parser.add_argument('trip_id', type=int, help='This field cannot be blank', required=True)
request_parser.add_argument('username', help='This field cannot be blank', required=True)
request_parser.add_argument('time_added', help='This field cannot be blank', required=False)


class ListRideOffers(Resource):
    """A view to list all ride offers and individual rides"""

    @jwt_required
    def get(self):
        return jsonify({'rides': models.trip_offers})


class GetRideOffer(Resource):
    """Get a specific ride offer by ride id"""

    @jwt_required
    def get(self, offer_id):
        for offer in models.trip_offers:
            if offer['id'] == offer_id:
                return {'ride-offer': offer}, 200
            else:
                if models.trip_offers.index(offer) == len(models.trip_offers) - 1:
                    return {
                               'message': 'trip offer not found'
                           }, 204


class AddRideOffer(Resource):
    @jwt_required
    def post(self):
        data = ride_parser.parse_args()
        ride_id = len(models.trip_offers) + 1
        data['id'] = ride_id
        data['time_added'] = time.strftime("%c")
        tmp = models.trip_offers
        # append data to the existing list
        tmp.append(data)
        return {
                   'item': data,
               }, 201


########################################################################################################
class GetRideRequests(Resource):
    # @jwt_required
    def get(self, offer_id):
        """
        get a list of ride requests made for a specific ride
        :param offer_id:
        :return request, ride:
        """
        if type(offer_id) == int:
            try:
                ride_req = [r for r in models.trip_requested if r['trip_id'] == offer_id]
                ride = [r for r in models.trip_offers if r['id'] == offer_id]

                return {
                           'requests': ride_req,
                           'ride': ride,
                       }, 200
            except:
                return {'message': "ride not found"}, 204
        else:
            return {'Invalid Input': "Input has to be an integer"}, 400


class AddRideRequest(Resource):
    """Get a specific ride request by request id"""

    @jwt_required
    def post(self, offer_id):
        try:
            username = get_jwt_identity()
        except:
            return {'error': 'session data not available'}
        if username is None:
            return {
                'message': 'Please Login to recapture session data',
                'details': 'The server instance seems to have restarted but'
                           ' credentials from the previous session are being used. his is a bug that is as a result '
                           'of non-persistent memory for now'
            }

        data = dict(
            id=len(models.trip_requested)+1,
            trip_id=offer_id,
            requester=username,
            time=time.strftime("%c")
        )
        models.trip_requested.append(data)  # append data to list
        return {
            'message': 'Trip request created',
            'details': data
        }


class ListRideRequests(Resource):
    """A view to list all ride requests """

    @jwt_required
    def get(self):
        return jsonify({'rides': models.trip_requested})
