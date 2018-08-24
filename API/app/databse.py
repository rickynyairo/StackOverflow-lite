"""
This module sets up the database that will be used
"""
import psycopg2
from contextlib import closing
import os
from . import APP

def init_db(url):
    """Set up the database to stode the user data
    """
    db_url = url  
    conn = psycopg2.connect(db_url)
    return conn


def connect_to(url):
    conn = psycopg2.connect(url)
    return conn

def init_test_db():
    conn = connect_to(os.getenv('DATABASE_TEST_URL'))
    with closing(conn) as conn, conn.cursor() as cursor:
        with APP.open_resource('stackovflow.sql', mode='r') as sql:
            cursor.execute(sql.read())
        conn.commit()
        return conn

def destroy_test():
    test_url = os.getenv('DATABASE_TEST_URL')
    curr = connect_to(test_url).cursor()   
    queries = [
        "DROP TABLE IF EXISTS comments CASCADE",
        "DROP TABLE IF EXISTS answers CASCADE",
        "DROP TABLE IF EXISTS questions CASCADE",
        "DROP TABLE IF EXISTS users CASCADE"
    ]
    for query in queries:
        curr.execute(query)
