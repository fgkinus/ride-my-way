from flask_restplus import fields

# models
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
