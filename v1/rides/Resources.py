import datetime
import time
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restplus import Resource, reqparse, fields, marshal_with
from werkzeug.debug import console

from v1 import connect_db, users
from db.utils import query_db

# def database connection
# database connection
DB = connect_db()
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

    @users.api.doc(params={'none': 'get request with no parameters'})
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

    @users.api.doc(params={'id': 'The ride Id'})
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

    @jwt_required
    @users.api.doc(params={'id': 'The ride offer id to delete'})
    def delete(self, offer_id):
        """
        delete a ride offer if you are the owner
        :param offer_id:
        :return:
        """
        # first get the ride
        query = """SELECT * FROM trips WHERE id=%s"""
        param = (offer_id,)
        try:
            ride_offer = query_db(conn=DB[0], query=query, args=param)
        except:
            return jsonify(
                {
                    'message': ' Error getting ride '
                }
            ), 500
        # ensure a ride request exists
        if len(ride_offer) != 1:
            return {
                       "message": "Trip offer not Found"
                   }, 204
        # # verify the logged in user is the owner of the ride
        current_user = get_jwt_identity()
        try:
            if ride_offer[0]['driver'] != current_user:
                return {
                           'message': " sorry {} You are not authorised to remove this ride".format(current_user)
                       }, 401
        except:
            return {
                       "error": "Could not verify ride ownership",
                       "driver": ride_offer[0]['driver'],
                       'current_user': current_user
                   }, 401
        # delete the ride returning the deleted ride
        query = """DELETE FROM trips WHERE id = %s RETURNING *"""
        try:
            ride = query_db(conn=DB[0], query=query, args=(offer_id,))
            return {
                       'message': 'Record successfully deleted',
                   }, 200
        except:
            return jsonify(
                {
                    "message": "could not complete request"
                }
            ), 400


class AddRideOffer(Resource):
    @jwt_required
    @users.api.expect(ride_parser)
    def post(self):
        data = ride_parser.parse_args()
        # set the driver to current logged in user
        data['driver'] = get_jwt_identity()
        # verify user is a driver and can add rides
        get_user = """SELECT * FROM user_accounts WHERE username=%s"""
        user = query_db(conn=DB[0], query=get_user, args=(data['driver'],))

        try:
            if user[0]['user_type'] != 'driver':
                return {
                           "message": "Unauthorised operation",
                           "Details": "A passenger is not permitted to add trips"
                       }, 401
        except:
            return {
                       "error": "could not get current user details"
                   }, 401
        # add the use Trip to database
        query = """INSERT INTO trips (origin,destination,driver,route,vehicle_model,vehicle_capacty,departure_time)
                    VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id ;"""
        # default departure time variable
        depart = datetime.datetime.now(datetime.timezone.utc)
        data['departure_time'] = depart
        param = (data['origin'], data['destination'], data['driver'], data['route'], data['vehicle_model'],
                 data['vehicle_capacity'], data['departure_time'])
        # a try catch to handle errors arising from query execution
        try:
            id = query_db(DB[0], query, param)
            # convert date time to serializable object
            data['departure_time'] = depart.strftime('%c')
            data['time_added'] = data['departure_time']
            data['id'] = id[0]['id']
            return {
                       'message': "new trip added",
                       'trip': data,
                   }, 201
        except:
            return {
                       'message': 'Error adding Ride',
                   }, 500


########################################################################################################
class GetRideRequests(Resource):
    # @jwt_required
    def get(self, offer_id):
        """
        get a list of ride requests made for a specific ride
        :param offer_id:
        :return request, ride:
        """
        query = """SELECT * FROM trips WHERE id=%s"""
        param = (offer_id,)
        try:
            ride_offer = query_db(conn=DB[0], query=query, args=param)
        except:
            return jsonify(
                {
                    'message': ' Error getting ride '
                }
            ), 500
        # ensure a ride request exists
        if len(ride_offer) != 1:
            return {
                       "message": "Trip offer not Found"
                   }, 204
        # now get ride requests for the offer
        query = """SELECT
                  tr.id,
                  a.username,
                  tr.created
                FROM trip_requests tr
                  INNER JOIN user_accounts a ON tr.requester = a.id
                WHERE tr.trip_id = 1"""
        try:
            requests = query_db(DB[0], query, (offer_id,))
            return jsonify(
                {
                    "requests": requests,
                    'ride-details': ride_offer
                }
            )
        except:
            return {
                       "message": "could not fetch ride requests"
                   }, 500


class AddRideRequest(Resource):
    """Get a specific ride request by request id"""

    @jwt_required
    def post(self, offer_id):
        try:
            username = get_jwt_identity()
        except:
            return {'error': 'session data not available'}
        # queries
        query_id = "SELECT id FROM user_accounts WHERE username= %s;"
        query_offer = "SELECT * FROM trips WHERE id= %s;"
        query_insert = """INSERT INTO trip_requests(trip_id, requester) VALUES (%s,%s) returning *;"""
        # run queries
        ride_offer = query_db(DB[0], query_offer, (offer_id,))
        user_id = query_db(DB[0], query_id, (username,))

        if len(ride_offer) != 1:
            return {
                       "message": "ride offer not found"
                   }, 204

        if len(user_id) == 1:
            user_id = user_id[0]['id']

        param = (offer_id, user_id)
        request = query_db(DB[0], query_insert, param)

        return make_response(
            jsonify(
                {
                    "message": "Trip added",
                    "request": request
                }
            ), 201
        )


class ListRideRequests(Resource):
    """A view to list all ride requests """

    @jwt_required
    def get(self):
        query = """SELECT
                  tr.id,
                  tr.trip_id,
                  a.username,
                  tr.created
                FROM trip_requests tr
                  INNER JOIN user_accounts a ON tr.requester = a.id """

        requests = query_db(DB[0], query, None)
        return jsonify(
            {
                "requests": requests
            }
        )


########################################################################################################
class RespondToRequest(Resource):
    """ Add responses to ride requests for drivers"""

    @jwt_required
    def post(self, req_id, response):
        query_add_response = """INSERT INTO request_responses(request_id, response) VALUES (%s,%s) returning *;"""
        query_get_request = """SELECT
                              tr.trip_id,
                              t.driver
                            FROM trip_requests tr
                              INNER JOIN trips t ON tr.trip_id = t.id
                            WHERE tr.id = %s"""
        try:
            request = query_db(DB[0], query_get_request, (req_id,))
        except:
            return {"error": "Could not fetch trip"}
        # verify request exists
        if len(request) != 1:
            return {}, 204
        # verify current user owns the trip and can accept request
        if request[0]['driver'] != get_jwt_identity():
            return {"message": "Unauthorised operation"}, 401
        # Add response to DB
        try:
            added_response = query_db(DB[0], query_add_response, (req_id, response))
            return jsonify(
                {
                    'message': 'Response recorded',
                    'response': added_response
                }
            )
        except:
            return {
                       "message": "Error adding response",
                       "details": "Check that response is valid ie {} or {}".format('Reject', 'Accept'),
                       "more-details": "If response has previously been made the operation will fail too"
                   }, 400


class GetRequestResponse(Resource):
    """ a resource to handle urls for request responses"""

    @jwt_required
    def get(self, req_id):
        query = """SELECT * FROM request_responses WHERE request_id = %s"""
        try:
            response = query_db(DB[0], query, (req_id,))
        except:
            return {'error': "couldn't fetch response to request"}
        # verify responses are present
        if len(response) != 1:
            return {}, 204
        # return response to request
        return jsonify({'response': response})
