from psycopg2.extras import RealDictCursor


def close(cursor, connection):
    cursor.close()
    connection.close()


def query_db(conn, query, args):
    """
    a custom function to run any valid SQL query provided a connection object is provided.
    If a transaction fails , its rolled back and cursors are not blocked
    :param conn:
    :param query:
    :param args:
    :return result:
    """
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, args)
            result = cur.fetchall()
            return result


# def check_db_exists(db_name='rmw'):
#     """Verify that db exists"""
#     try:
#         conn = connect('pg_catalog.pg_database', 'postgres', password='')
#         cur = conn.cursor()
#         result = cur.execute("""select exists(
#                      SELECT {0} FROM pg_catalog.pg_database WHERE lower({0}) = lower({0})
#                     );""".format(db_name))
#         if result is True:
#             return True
#         else:
#             return False
#
#     except Exception:
#         print("Could not connect to db")
#     return False


# queries
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
);
"""

# run queries to create tables
