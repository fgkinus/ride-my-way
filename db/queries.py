user_account_create = """CREATE TABLE user_accounts
(
  id          SERIAL NOT NULL
    CONSTRAINT user_accounts_pkey
    PRIMARY KEY,
  first_name  VARCHAR NOT NULL,
  second_name VARCHAR NOT NULL,
  username    VARCHAR NOT NULL,
  email       VARCHAR NOT NULL,
  password    VARCHAR NOT NULL,
  user_type   VARCHAR NOT NULL
);
CREATE UNIQUE INDEX user_accounts_username_uindex
  ON user_accounts (username);

CREATE UNIQUE INDEX user_accounts_email_uindex
  ON user_accounts (email);
                """
trip_offers_create = """CREATE TABLE trips
(
  id              SERIAL NOT NULL
    CONSTRAINT id
    PRIMARY KEY,
  origin          TEXT    NOT NULL,
  destination     TEXT,
  departure_time  TIMESTAMP WITH TIME ZONE,
  vehicle_model   TEXT,
  vehicle_capacty INTEGER,
  route           TEXT,
  time_aded       TIME WITH TIME ZONE,
  driver          TEXT
    CONSTRAINT trips_user_accounts_username_fk
    REFERENCES user_accounts (username)
    ON UPDATE CASCADE ON DELETE CASCADE
);"""
trip_requests_create = """CREATE TABLE trip_requests
(
  id        SERIAL NOT NULL
    CONSTRAINT trip_requests_pkey
    PRIMARY KEY,
  trip_id   INTEGER NOT NULL
    CONSTRAINT trip_requests_trips_id_fk
    REFERENCES trips
    ON UPDATE CASCADE ON DELETE CASCADE,
  requester INTEGER NOT NULL
    CONSTRAINT trip_requests_user_accounts_id_fk
    REFERENCES user_accounts
    ON UPDATE CASCADE ON DELETE CASCADE
);"""
rides_given_create = """CREATE TABLE rides_given
(
  id      SERIAL NOT NULL
    CONSTRAINT rides_given_pkey
    PRIMARY KEY,
  ride_id INTEGER
    CONSTRAINT rides_given_trips_id_fk
    REFERENCES trips
    ON UPDATE CASCADE ON DELETE CASCADE
);"""
notifications_create = """CREATE TABLE notifications
(
  id       SERIAL NOT NULL
    CONSTRAINT notifications_id_pk
    PRIMARY KEY,
  trip_id INTEGER
    CONSTRAINT notifications_trips_id_fk
    REFERENCES trips
    ON UPDATE CASCADE ON DELETE CASCADE,
  action  TEXT,
  time    TIMESTAMP
);
CREATE UNIQUE INDEX notifications_id_uindex
  ON notifications (id);
"""
jwt_black_list_create = """CREATE TABLE jwt_blacklist
(
  id   SERIAL       NOT NULL
    CONSTRAINT jwt_blacklist_pkey
    PRIMARY KEY,
  jwt  VARCHAR(255) NOT NULL,
  time TIMESTAMP DEFAULT now()
);"""
responses_table_create = """CREATE TABLE public.request_responses
(
  id         SERIAL PRIMARY KEY      NOT NULL,
  request_id INT                     NOT NULL,
  response   RESPONSE                NOT NULL,
  created    TIMESTAMP DEFAULT now() NOT NULL,
  CONSTRAINT request_responses_trip_requests_id_fk FOREIGN KEY (request_id) REFERENCES trip_requests (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX request_responses_request_id_uindex
  ON 
  public.request_responses (request_id);
"""
response = """CREATE TYPE RESPONSE AS ENUM ('Accept', 'Reject');"""


request_responses_create = """CREATE TABLE request_responses
(
  id         SERIAL                  NOT NULL
    CONSTRAINT request_responses_pkey
    PRIMARY KEY,
  request_id INTEGER                 NOT NULL
    CONSTRAINT request_responses_trip_requests_id_fk
    REFERENCES trip_requests
    ON UPDATE CASCADE ON DELETE CASCADE,
  response   RESPONSE                NOT NULL,
  created    TIMESTAMP DEFAULT now() NOT NULL
);

CREATE UNIQUE INDEX request_responses_request_id_uindex
  ON request_responses (request_id);

"""

# tables = dict(
#     user_accounts=user_account_create,
#     trip_offrs=trip_requests_create,
#     trip_requests=trip_requests_create,
#     rides_given=rides_given_create,
#     notifications=notifications_create,
#     black_list=jwt_black_list_create,
#     requst_responses=request_responses_create,
# )
tables_list = [
    jwt_black_list_create,response,user_account_create, trip_offers_create, trip_requests_create,notifications_create,
    request_responses_create,rides_given_create
]
