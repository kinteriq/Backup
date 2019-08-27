import os
import pytest
import sqlite3
from unittest import mock

from backup import shortcuts
from .fixtures import PATH

CREATE_ARGS = ['NAME', 'SOURCE', 'DEST', '...']
DELETE_ARGS = [CREATE_ARGS[0], 'wrong_NAME']
SHOW_ARGS = [CREATE_ARGS[0], 'wrong_NAME']


def setup_module():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    connection.commit()
    connection.close()


def teardown_module():
    os.remove(PATH)


def test_shortcut_is_created():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')
    expected_result = tuple(CREATE_ARGS[:2] + [', '.join(CREATE_ARGS[2:])])
    for row in selection:
        assert expected_result == row


def test_update_shortcut(monkeypatch):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    # shortcuts.create(args=CREATE_ARGS, datapath=PATH)     # TODO make independant
    with mock.patch('builtins.input', side_effect=['changed/path', '']):
        shortcuts.update(args=[CREATE_ARGS[0]], datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')
    expected_result = tuple([CREATE_ARGS[0]] + ['changed/path'] +
                            [', '.join(CREATE_ARGS[2:])])
    for row in selection:
        assert expected_result == row


def test_delete_shortcut():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    shortcuts.delete(args=DELETE_ARGS, datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')  # TODO adjust
    for row in selection:
        assert not row


def test_show_shortcut():
    assert fail


def test_showall():
    assert fail
