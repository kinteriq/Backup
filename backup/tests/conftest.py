import pytest
import os
import shutil
import sqlite3

from constants import SHORTCUT_NAMES, DB


@pytest.fixture
def mock_fields_db(DB_PATH):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    first_name = (SHORTCUT_NAMES[0], DB['source'], DB['destination'])
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', first_name)
    second_name = (SHORTCUT_NAMES[1], DB['source'], DB['another_destination'])
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', second_name)
    connection.commit()
    connection.close()
    yield DB_PATH


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
def DB_PATH():
    yield os.path.join(os.getcwd(), 'test.db')
    try:
        os.remove(os.path.join(os.getcwd(), 'test.db'))
    except FileNotFoundError:
        pass


@pytest.fixture(autouse=True)
def rm_destination_dir():
    try:
        shutil.rmtree(DB['destination'])
    except FileNotFoundError:
        pass