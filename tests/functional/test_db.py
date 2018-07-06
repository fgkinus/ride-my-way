# import os
#
# import psycopg2
# import pytest
# from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#
# from db import utils
# from db.utils import Database
#
#
# class TestDB(object):
#     def test_connection(self, test_db):
#         """Test connection to the test DB"""
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = test_db.connect_db(db_name=db_name, username=user, password=password)
#
#         assert db_name is not None
#         assert user is not None
#         assert isinstance(conn, psycopg2.extensions.connection)
#         assert conn.closed == 0
#         # test connection closing
#         conn = conn.close()
#         assert conn.closed == 1
#
#     def test_query(self, test_db):
#         valid_query = """SELECT datname FROM  pg_database;"""
#         invalid_query = """SELECT datnamems FROM  pg_database where ;"""
#
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = test_db.connect_db(db_name=db_name, username=user, password=password)
#         response = test_db.query_db(valid_query, ())
#         assert isinstance(response, list)
#
#         with pytest.raises(psycopg2.DatabaseError):
#             test_db.query_db(invalid_query, ())
#
#         conn.close()
#
#     def test_create_db_and_delete_db(self, test_db):
#         db_name = os.getenv('TESTING_DB_NAME')
#         user = os.getenv('TESTING_DB_USER')
#         password = os.getenv('TESTING_DB_PASSWORD')
#         conn = test_db.connect_db(db_name=db_name, username=user, password=password)
#
#         new_db_name = 'new_testing_db'
#         test_db.create_db(conn, new_db_name)
#         assert conn.closed == 1
#
#         conn = psycopg2.connect(database=db_name, user=user, password=password)
#         assert test_db.check_db_exists(db_name=new_db_name)[0]['exists'] is True
#
#         query = """drop database new_testing_db;"""
#         with conn:
#             conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#             with conn.cursor() as cur:
#                 cur.execute(query)
#
#         assert test_db.check_db_exists(db_name=new_db_name)[0]['exists'] is False
#         conn.close()
#         assert conn.closed == 1
