import os
import pytest
import sqlite3

from .fixtures import PATH, SOURCE, DESTINATION
from backup import copyrun

DATA_1 = ('testing', SOURCE, DESTINATION)


def setup_module():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', DATA_1)
    connection.commit()
    connection.close()


def teardown_module():
    os.remove(PATH)
    # TODO change
    os.rmdir(DESTINATION)


def test_copyall_ok():
    assert copyrun.call(['testing'], PATH) is True


@pytest.mark.skip('FINISH')
def test_copy_with_replacements():
    finish
