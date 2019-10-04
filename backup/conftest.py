import pytest
import os
import shutil
import sqlite3

from tests.constants import CREATE_1, CREATE_2, DESTINATIONS, PATH


@pytest.fixture(autouse=True)
def rm_destination_dir():
    for dst in DESTINATIONS:
        try:
            shutil.rmtree(dst)
        except FileNotFoundError:
            pass


@pytest.fixture
def DB_PATH():
    yield PATH
    try:
        os.remove(PATH)
    except FileNotFoundError:
        pass


@pytest.fixture
def empty_db_cursor(DB_PATH):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    yield cursor
    connection.commit()
    connection.close()


@pytest.fixture
def mock_fields_db(DB_PATH):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    first_row = (CREATE_1.name,
                 CREATE_1.source,
                 ', '.join(CREATE_1.destinations))
    second_row = (CREATE_2.name,
                  CREATE_2.source,
                  ', '.join(CREATE_2.destinations))
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', first_row)
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', second_row)
    connection.commit()
    connection.close()
    yield DB_PATH


@pytest.fixture
def mock_fields_db_cursor(mock_fields_db):
    connection = sqlite3.connect(mock_fields_db)
    cursor = connection.cursor()
    yield cursor
    connection.commit()
    connection.close()