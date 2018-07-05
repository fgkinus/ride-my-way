import os

import psycopg2
import pytest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from db import utils
from db.utils import close, query_db, create_db, check_db_exists


# class TestDB(object):
#     def test_connection(self):
#         """Test connection to the test DB"""
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = psycopg2.connect(database=db_name, user=user, password=password)
#
#         assert db_name is not None
#         assert user is not None
#         assert isinstance(conn, psycopg2.extensions.connection)
#         assert conn.closed == 0
#         # test connection closing
#         conn = close(conn)
#         assert conn.closed == 1
#
#     def test_query(self):
#         valid_query = """SELECT datname FROM  pg_database;"""
#         invalid_query = """SELECT datnamems FROM  pg_database where ;"""
#
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = psycopg2.connect(database=db_name, user=user, password=password)
#         response = query_db(conn, valid_query, ())
#         assert isinstance(response, list)
#
#         with pytest.raises(psycopg2.DatabaseError):
#             query_db(conn, invalid_query, ())
#
#         close(conn)
#
#     def test_create_db_and_delete_db(self):
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = psycopg2.connect(database=db_name, user=user, password=password)
#
#         new_db_name = 'new_testing_db'
#         create_db(conn, new_db_name)
#         assert conn.closed == 1
#
#         conn = psycopg2.connect(database=db_name, user=user, password=password)
#         assert check_db_exists(conn, db_name=new_db_name)[0]['exists'] is True
#
#         query = """drop database new_testing_db;"""
#         with conn:
#             conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#             with conn.cursor() as cur:
#                 cur.execute(query)
#
#         assert check_db_exists(conn, db_name=new_db_name)[0]['exists'] is False
#         close(conn)
#         assert conn.closed == 1
