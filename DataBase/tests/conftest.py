import pytest
import psycopg2

@pytest.fixture(scope='module')
def db_connection():
    conn = psycopg2.connect(
        dbname='EMarket',
        user='admin',
        password='password',
        host='localhost',
        port='5433'
    )
    yield conn
    conn.close()

@pytest.fixture(scope='module')
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
