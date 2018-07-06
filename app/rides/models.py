from flask_restplus import fields
import datetime
from dateutil.parser import parse

# models
from app.users.models import User
from app.utils import Database

ride_fields = {
    "departure_time": fields.String,
    "destination": fields.String,
    "driver": fields.String,
    "id": fields.Integer,
    "origin": fields.String,
    "route": fields.String,
    "time_aded": fields.String,
    "vehicle_capacty": fields.Integer,
    "vehicle_model": fields.String
}


class Ride(object):
    """a class representing a ride instance"""

    def __init__(self, data=None, database=Database):
        """initialise the ride object with a DB instance and parsed data"""
        self.DB = database
        self.details = data

    def list_all_rides(self):
        query = """SELECT * FROM trips"""
        ride_offers = self.DB.query_db(query=query, args=())
        # convert the time stamps to json serializable format
        for ride in ride_offers:
            ride['time_added'] = ride['time_added'].strftime('%c')
        return ride_offers

    def add_ride(self, current_user):
        """add a new ride offer"""
        get_user = """SELECT * FROM user_accounts WHERE username=%s"""
        user = self.DB.query_db(query=get_user, args=(current_user,))
        if user[0]['user_type'] != 'driver':
            return False
        # add the use Trip to database
        query = """INSERT INTO trips (origin,destination,driver,route,vehicle_model,vehicle_capacty,departure_time)
                                VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id ;"""
        data = self.details
        depart = datetime.datetime.now(datetime.timezone.utc)
        try:
            time = parse(data['departure_time'])
            data['departure_time'] = time
        except:
            data['departure_time'] = depart
        param = (data['origin'], data['destination'], data['driver'], data['route'], data['vehicle_model'],
                 data['vehicle_capacity'], data['departure_time'])
        ride_id = self.DB.query_db(query, param)
        data['departure_time'] = data['departure_time'].strftime('%c')
        data['time_added'] = depart.strftime('%c')
        data['id'] = ride_id[0]['id']
        return data

    def get_ride(self, offer_id):
        query = """SELECT * FROM trips WHERE id=%s"""
        param = (offer_id,)
        ride_offer = self.DB.query_db(query=query, args=param)
        return ride_offer

    def delete_ride(self, ride_id, current_user):
        ride_offer = self.get_ride(ride_id)
        if len(ride_offer) != 1:
            return False, 1
        if ride_offer[0]['driver'] != current_user:
            return False, 2
        query = """DELETE FROM trips WHERE id = %s RETURNING *"""
        ride = self.DB.query_db(query=query, args=(ride_id,))
        return ride

    def get_ride_request(self, ride_id):
        ride_offer = self.get_ride(ride_id)
        if len(ride_offer) != 1:
            return False
        query = """SELECT
                          tr.id,
                          a.username,
                          tr.created
                        FROM trip_requests tr
                          INNER JOIN user_accounts a ON tr.requester = a.id
                        WHERE tr.trip_id = %s"""
        requests = self.DB.query_db(query, (ride_id,))
        return requests, ride_offer

    def add_ride_request(self, ride_id, username):
        user = User()
        user_id = user.get_user(username=username)[0]['id']
        ride = self.get_ride(ride_id)
        if len(ride) != 1:
            return False
        query_insert = """INSERT INTO trip_requests(trip_id, requester) VALUES (%s,%s) returning *;"""
        param = (ride_id, user_id)

        trip_request = self.DB.query_db(query=query_insert, args=param)
        return trip_request

    def remove_ride_request(self, req_id, username):
        query_request = """delete from trip_requests  where id =%s
                            and requester= (select id from user_accounts where username = %s) returning  *;"""
        param = (req_id, username)

        ride_req = self.DB.query_db(query=query_request, args=param)
        return ride_req

    def list_ride_request(self):
        query = """SELECT
                          trips.id,
                          trips.trip_id,
                          account.username,
                          trips.created
                        FROM trip_requests trips
                          INNER JOIN user_accounts account ON trips.requester = account.id """
        requests = self.DB.query_db(query, ())
        return requests

    def respond_to_request(self, req_id, response, current_user):
        request = self.get_ride_request(req_id)
        if len(request) != 1:
            return False, 1
        if request[0]['driver'] != current_user:
            return False, 2
        query_add_response = """INSERT INTO request_responses(request_id, response) VALUES (%s,%s) returning *;"""
        added_response = self.DB.query_db(query_add_response, (req_id, response))
        return added_response

    def get_req_response(self, req_id):
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
        response = self.DB.query_db(query, (req_id,))
        return response
