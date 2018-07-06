import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor

from db import queries


#
#
# def close(connection):
#     connection.close()
#     return connection
#
#
# def query_db(conn, query, args):
#     """
#     a custom function to run any valid SQL query provided a connection object is provided.
#     If a transaction fails , its rolled back and cursors are not blocked
#     :param conn:
#     :param query:
#     :param args:
#     :return result:
#     """
#     with conn:
#         with conn.cursor(cursor_factory=RealDictCursor) as cur:
#             cur.execute(query, args)
#             result = cur.fetchall()
#             return result
#
#
# def add_table(conn, query):
#     """
#     a custom function to run any valid SQL query provided a connection object is provided.
#     If a transaction fails , its rolled back and cursors are not blocked
#     :param conn:
#     :param query:
#     :return:
#     """
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(query)
#
#
# def create_tables(conn, queries):
#     for query in queries:
#         add_table(conn=conn, query=query)
#
#
# def check_db_exists(conn, db_name='rmw'):
#     """Verify that db exists"""
#     query = """select exists(
#              SELECT datname FROM pg_catalog.pg_database WHERE datname=%s
#             );
#             """
#     return query_db(conn, query, (db_name,))
#
#
# def create_db(conn, dbname):
#     query = """CREATE DATABASE {} ENCODING ='utf8'""".format(dbname)
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(query)
#     conn.close()


class Database(object):

    def __init__(self, username, password, db_name):
        self.username = username
        self.password = password
        self.db_name = db_name
        self.conn = None

    @staticmethod
    def connect_db(db_name, username, password):
        try:
            conn = psycopg2.connect(database=db_name, user=username, password=password)
            return conn
        except Exception:
            raise psycopg2.DatabaseError("could not connect to database")

    def get_connection(self):
        if isinstance(self.conn, psycopg2.extensions.connection):
            return self.conn
        else:
            raise ConnectionError("connection not established.please initialise the DB first")

    def create_db(self, dbname, username, password):
        query = """CREATE DATABASE {} ENCODING ='utf8'""".format(dbname)
        conn = self.connect_db('postgres', username, password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.query_db_no_result(query, ())
        conn.close()

    def create_tables(self, conn, create_queries=queries.tables_list):
        for query in create_queries:
            self.query_db_no_result(query=query, args=())

    def query_db(self, query, args):
        """
        a custom function to run any valid SQL query provided a connection object is provided.
        If a transaction fails , its rolled back and cursors are not blocked
        :param conn:
        :param query:
        :param args:
        :return result:
        """
        conn = self.get_connection()
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute(query, args)
                except:
                    raise psycopg2.DatabaseError
                result = cur.fetchall()
                return result

    def query_db_no_result(self, query, args):
        """
        a custom function to run any valid SQL query provided a connection object is provided.
        If a transaction fails , its rolled back and cursors are not blocked
        :param query:
        :param args:
        :return :
        """
        conn = self.get_connection()
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, args)

    def check_db_exists(self, db_name='rmw'):
        """Verify that db exists"""
        query = """select exists(
                 SELECT datname FROM pg_catalog.pg_database WHERE datname=%s
                );
                """
        return self.query_db(query, (db_name,))

    def close_conn(self):
        self.conn.close()
        return self.conn

    def init_db(self):
        """initialise database"""
        # create db connecton to root db
        self.conn = self.connect_db(db_name='postgres', username=self.username, password=self.password)
        # verify db exists
        if self.check_db_exists(db_name=self.db_name)[0]['exists']:
            # set connection
            self.conn = self.connect_db(db_name=self.db_name, username=self.username, password=self.password)
            return self
        else:
            # create db and initialise connection
            self.create_db(self.db_name, password=self.password, username=self.username)
            self.conn = self.connect_db(db_name=self.db_name, username=self.password, password=self.password)
            self.create_tables(conn=self.conn)
            return self
