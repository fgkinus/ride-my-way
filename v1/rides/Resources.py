import datetime
import time
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, reqparse, fields, marshal_with


from v1 import connect_db
from v1.rides import models
from db.utils import query_db

# def database connection
# database connection
DB = connect_db('rmw', 'postgres', '')
cursor = DB[1]

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
        query = """SELECT * FROM trips"""
        try:
            ride_offers = query_db(conn=DB[0], query=query, args=None)
            return jsonify(
                {
                    'ride-offers': ride_offers
                }
            )
        except:
            return {
                       'message': ' Error getting rides list'
                   }, 500


class GetRideOffer(Resource):
    """Get a specific ride offer by ride id"""

    @jwt_required
    def get(self, offer_id):
        query = """SELECT * FROM trips WHERE id=%s"""
        param = (offer_id,)
        try:
            ride_offer = query_db(conn=DB[0], query=query, args=param)
            return jsonify(
                {
                    'ride-offers': ride_offer
                }
            )
        except:
            return {
                       'message': ' Error getting ride list'
                   }, 500


class AddRideOffer(Resource):
    @jwt_required
    def post(self):
        data = ride_parser.parse_args()
        query = """INSERT INTO trips (origin,destination,driver,route,vehicle_model,vehicle_capacty,departure_time)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);"""

        depart = datetime.datetime.now(datetime.timezone.utc)
        data['departure_time'] = depart
        param = (data['origin'], data['destination'], data['driver'], data['route'], data['vehicle_model'],
                 data['vehicle_capacity'], data['departure_time'])
        query_db(DB[0], query, param)


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
            id=len(models.trip_requested) + 1,
            trip_id=offer_id,
            requester=username,
            time=time.strftime("%c")
        )
        models.trip_requested.append(data)  # append data to list
        return {
                   'message': 'Trip request created',
                   'details': data
               }, 201


class ListRideRequests(Resource):
    """A view to list all ride requests """

    @jwt_required
    def get(self):
        return jsonify({'rides': models.trip_requested})


########################################################################################################
class RespondToRequest(Resource):
    """ Add responses to ride requests for drivers"""

    @jwt_required
    def post(self, req_id, response):
        req = [req for req in models.trip_requested if req['id'] == req_id]
        if len(req) == 1:
            response = dict(
                id=len(models.request_respons) + 1,
                req_id=req_id,
                response=response
            )
            models.request_respons.append(response)
            return jsonify({
                'request': req[0]
            }), 201
        else:
            return jsonify(
                {
                    'message': 'ride not found'
                }, 200
            )
