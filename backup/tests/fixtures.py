import pytest
import os
import sqlite3


# TODO os.rmdir(DESTINATION)
# TODO remove vars

# PATH = os.path.join(os.getcwd(), 'test.db') # TODO fixtures using PATH fixture
SHORTCUT_NAMES = ('TEST_1', 'TEST_2')
SOURCE = os.path.join(os.getcwd(), 'backup')
DESTINATION = os.path.join(os.getcwd(), 'testBackup')
ANOTHER_DESTINATION = os.path.join(os.getcwd(), 'testBackup_2')


@pytest.fixture
def mock_fields_db(PATH):   # TODO unite with empty_db_cursor
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    first_name = (SHORTCUT_NAMES[0], 'from/path_1', 'to/path_1')
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', first_name)
    second_name = (SHORTCUT_NAMES[1], 'from/path_2', 'to/path_2')
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', second_name)
    connection.commit()
    connection.close()
    yield connection
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
    return os.path.join(os.getcwd(), 'test.db')
