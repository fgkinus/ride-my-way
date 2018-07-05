from flask_restplus import fields


# models
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
