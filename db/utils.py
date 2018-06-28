import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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


def add_table(conn, query):
    """
    a custom function to run any valid SQL query provided a connection object is provided.
    If a transaction fails , its rolled back and cursors are not blocked
    :param conn:
    :param query:
    :return:
    """
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)


def create_tables(conn, queries):
    for query in queries:
        add_table(conn=conn, query=query)


def check_db_exists(conn, db_name='rmw'):
    """Verify that db exists"""
    query = """select exists(
             SELECT datname FROM pg_catalog.pg_database WHERE datname=%s
            );
            """
    return query_db(conn, query, (db_name,))


def create_db(conn, dbname):
    query = """CREATE DATABASE {} ENCODING ='utf8'""".format(dbname)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
    conn.close()