"""Sample Project Data"""

notifications = [
    {
        "from": "jsmith",
        "id": 3,
        "trip_id": 5,
        "action": "accepted",
        "time": "2018-06-15 06:56:54.459000"
    },
    {
        "from": "jsmith",
        "id": 2,
        "trip_id": 3,
        "action": "rejecte",
        "time": "2018-06-15 06:56:52.584000"
    },
    {
        "from": "jdoe",
        "id": 5,
        "trip_id": 4,
        "action": "accepted",
        "time": "2018-06-15 10:57:17.896000"
    },
    {
        "from": "jsmith",
        "id": 1,
        "trip_id": 2,
        "action": "accepted",
        "time": "2018-06-15 06:56:29.943000"
    },
    {
        "from": "jdoe",
        "id": 4,
        "trip_id": 1,
        "action": "accepted",
        "time": "2018-06-15 19:59:58.381000"
    }
]
rides_given = [
    {
        "id": 1,
        "ride_id": 1,
        "driver_id": 1
    },
    {
        "id": 2,
        "ride_id": 3,
        "driver_id": 1
    },
    {
        "id": 3,
        "ride_id": 2,
        "driver_id": 2
    },
    {
        "id": 4,
        "ride_id": 4,
        "driver_id": 3
    },
    {
        "id": 5,
        "ride_id": 6,
        "driver_id": 2
    },
    {
        "id": 6,
        "ride_id": 5,
        "driver_id": 1
    }
]
rides_taken = [
    {
        "ride_id": 1,
        "id": 1,
        "passenger_id": 1
    },
    {
        "ride_id": 1,
        "id": 2,
        "passenger_id": 3
    },
    {
        "ride_id": 1,
        "id": 3,
        "passenger_id": 2
    },
    {
        "ride_id": 4,
        "id": 4,
        "passenger_id": 2
    },
    {
        "ride_id": 3,
        "id": 5,
        "passenger_id": 2
    },
    {
        "ride_id": 4,
        "id": 6,
        "passenger_id": 1
    },
    {
        "ride_id": 5,
        "id": 7,
        "passenger_id": 3
    },
    {
        "ride_id": 6,
        "id": 8,
        "passenger_id": 1
    }
]
trip_requested = [
    {
        "id": 1,
        "trip_id": 1,
        "requester": "psycho"
    },
    {
        "id": 2,
        "trip_id": 1,
        "requester": "jripper"
    },
    {
        "id": 3,
        "trip_id": 2,
        "requester": "psycho"
    },
    {
        "id": 4,
        "trip_id": 3,
        "requester": "psycho"
    },
    {
        "id": 5,
        "trip_id": 4,
        "requester": "jripper"
    }
]
trip_offers = [
    {
        "id": 4,
        "origin": "cbd",
        "destination": "westlands",
        "departure_time": "2018-06-12 18:11:40.984000",
        "vehicle_model": "fielder",
        "vehicle_capacty": 5,
        "route": "waiyaki way]",
        "time_aded": None,
        "driver": "jdoe"
    },
    {
        "id": 3,
        "origin": "yaya",
        "destination": "cbd",
        "departure_time": "2018-06-11 23:11:20.109000",
        "vehicle_model": "passat",
        "vehicle_capacty": 4,
        "route": "uhuhuru highway",
        "time_aded": None,
        "driver": "jsmith"
    },
    {
        "id": 2,
        "origin": "juja",
        "destination": "rosambu",
        "departure_time": "2018-06-15 18:11:04.828000",
        "vehicle_model": "passsat",
        "vehicle_capacty": 4,
        "route": "thika road",
        "time_aded": None,
        "driver": "jsmith"
    },
    {
        "id": 1,
        "origin": "ngara",
        "destination": "thika",
        "departure_time": "2018-05-14 18:10:46.703000",
        "vehicle_model": "fielder",
        "vehicle_capacty": 5,
        "route": "thika road",
        "time_aded": None,
        "driver": "jdoe"
    },
    {
        "id": 5,
        "origin": "kinoo",
        "destination": "westlands",
        "departure_time": "2018-06-12 06:12:03.031000",
        "vehicle_model": "passat",
        "vehicle_capacty": 4,
        "route": "wiyakiway",
        "time_aded": None,
        "driver": "jmsmith"
    }
]
request_respons = [
    {
        "id": 1,
        "req_id": 2,
        "response": "accepted"
    },
    {
        "id": 2,
        "req_id": 1,
        "response": "rejected"
    }
]

from v1 import db


class rideOffers(db.Model):
    """ This class represents the ride table"""

    __tablename__ = 'rideoffers'
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(255), nullable=False)
    destination = db.Column(db.String(255), nullable=False)
    departure_time = db.Column(db.DateTime, default = db.func.current_timestamp())
    vehicle_model = db.Column(db.String(255))
    vehicle_capacty: db.Column(db.Integer)
    route = db.Column(db.String(255))
    "time_aded": None,
