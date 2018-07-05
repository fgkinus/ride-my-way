from __future__ import absolute_import
import datetime
from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_restplus import Resource, reqparse, Namespace, fields
from db.utils import query_db

# define a namespace for rides
api = Namespace('rides', description='rides related operations')

# database connection
import run

DB = run.app.config['DATABASE_CONN']


# error handlers
@api.errorhandler(NoAuthorizationError)
def handle_no_auth_exception(error):
    """Handle ethe jwt required exception when none s provided"""
    return {'message': 'No authentication token provided'}, 401


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
        query = """SELECT * FROM trips"""
        ride_offers = query_db(conn=DB[0], query=query, args=())
        # convert the time stamps to json serializable format
        for ride in ride_offers:
            ride['time_added'] = ride['time_added'].strftime('%c')

        try:
            ride_offers = query_db(conn=DB[0], query=query, args=())
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
                   }, 500
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


@api.route('/rides/<offer_id>', endpoint='get-ride')
@api.doc('get a specific ride')
class GetRideOffer(Resource):
    """Get a specific ride offer by ride id"""

    @api.doc(params={'id': 'The ride Id'})
    @jwt_required
    def get(self, offer_id):
        """Fetch a specific ride"""
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
    @api.doc(params={'id': 'The ride offer id to delete'})
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
            ), 500


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
                WHERE tr.trip_id = %s"""
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

    @jwt_required
    def post(self, offer_id):
        """add a new ride request"""
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


@api.route('/rides/<req_id>/requests', endpoint='remove-ride-requests')
@api.doc('remove a specific ride', params={'req_id': 'An ID for ride request'})
class RemoveRequests(Resource):
    @jwt_required
    def delete(self, req_id):
        """delete a ride request if you own the ride"""
        query_request = """delete from trip_requests  where id =%s 
                            and requester= (select id from user_accounts where username = %s) returning  *;"""
        param = (req_id, get_jwt_identity())
        request = query_db(conn=DB[0], query=query_request, args=param)

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
        query = """SELECT
                  trips.id,
                  trips.trip_id,
                  account.username,
                  trips.created
                FROM trip_requests trips
                  INNER JOIN user_accounts account ON trips.requester = account.id """

        requests = query_db(DB[0], query, None)
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
        # query definition
        query_add_response = """INSERT INTO request_responses(request_id, response) VALUES (%s,%s) returning *;"""
        query_get_request = """SELECT
                              tr.trip_id,
                              t.driver
                            FROM trip_requests tr
                              INNER JOIN trips t ON tr.trip_id = t.id
                            WHERE tr.id = %s"""
        # fetch ride request instance
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


@api.route('/rides/<req_id>/response', endpoint='get-ride-response')
@api.doc('get a specific ride request response', params={'req_id': 'An ID for ride request'})
class GetRequestResponse(Resource):
    """ a resource to handle urls for request responses"""

    @jwt_required
    def get(self, req_id):
        """get response for rides if you are the requester or owner of ride"""
        query = """
                SELECT
              account.username,
              req_res.response,
              request.id trip_id,
              trips.driver
            FROM request_responses req_res INNER JOIN trip_requests request on req_res.request_id = request.id
              inner join user_accounts account on request.requester = account.id
              inner join trips on request.trip_id = trips.id
            where req_res.id = %s
                """
        try:
            response = query_db(DB[0], query, (req_id,))
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