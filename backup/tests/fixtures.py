import pytest
import os
import sqlite3


# TODO remove vars

# PATH = os.path.join(os.getcwd(), 'test.db') # TODO fixtures using PATH fixture
SHORTCUT_NAMES = ('TEST_1', 'TEST_2')
SOURCE = os.path.join(os.getcwd(), 'backup')
DESTINATION = os.path.join(os.getcwd(), 'testBackup12424325')
ANOTHER_DESTINATION = os.path.join(os.getcwd(), 'testBackup_2324u43857843584624734')


@pytest.fixture
def mock_fields_db(PATH):   # TODO unite with empty_db_cursor
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    first_name = (SHORTCUT_NAMES[0], SOURCE, DESTINATION)
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', first_name)
    second_name = (SHORTCUT_NAMES[1], SOURCE, ANOTHER_DESTINATION)
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', second_name)
    connection.commit()
    connection.close()
    yield PATH
    os.remove(PATH)


@pytest.fixture
def empty_db_cursor(PATH):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    yield cursor
    connection.commit()
    connection.close()
    os.remove(PATH)


@pytest.fixture
def PATH():
    yield os.path.join(os.getcwd(), 'test.db')
    try:
        os.remove(os.path.join(os.getcwd(), 'test.db'))
    except FileNotFoundError:
        pass
