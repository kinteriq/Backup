from io import StringIO
import os
import pytest
import sqlite3
from unittest import mock

from backup import shortcuts, outputs
from .fixtures import (PATH, SOURCE, DESTINATION, ANOTHER_DESTINATION,
    empty_db_cursor, mock_fields_db)

NAME = 'NAME-1'

ANOTHER_NAME = 'NAME-2'

CREATE_ARGS = [NAME, SOURCE, DESTINATION, ANOTHER_DESTINATION]

ANOTHER_CREATE_ARGS = [ANOTHER_NAME, SOURCE, DESTINATION]

DELETE_ARGS = [NAME, 'wrong_NAME']

DELETE_MANY_ARGS = [NAME, ANOTHER_NAME]

SHOW_ARGS = [NAME, 'wrong_NAME']

SHOWALL_ARGS = [NAME, ANOTHER_NAME]

WRONG_PATH_ARGS = [NAME, 'wrong_path', 'path']


def test_wrong_path_name(empty_db_cursor, PATH):
    with pytest.raises(SystemExit) as e:
        shortcuts.create(args=WRONG_PATH_ARGS, datapath=PATH)
        assert 'Directory does not exist' in e.exconly()


def test_shortcut_is_created(empty_db_cursor, PATH):
    expected_result = tuple(CREATE_ARGS[:2] + [', '.join(CREATE_ARGS[2:])])
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    selection = empty_db_cursor.execute('''SELECT * FROM shortcuts''')
    for row in selection:
        assert expected_result == row


def test_update_shortcuts(monkeypatch, empty_db_cursor, PATH):
    expected_output = outputs.update_msg(updated_lst=[NAME, ANOTHER_NAME])
    expected_db_change = [tuple(CREATE_ARGS[1:]), tuple(ANOTHER_CREATE_ARGS[1:])]
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        with mock.patch('builtins.input', side_effect=[
                '', ANOTHER_DESTINATION, '', DESTINATION]):
            shortcuts.update(args=[NAME, ANOTHER_NAME], datapath=PATH)
        assert mock_output.getvalue().rstrip().endswith(expected_output)
    selection = empty_db_cursor.execute('''SELECT * FROM shortcuts''')
    for row in selection:
        assert row[1:] in expected_db_change


def test_delete_shortcut(empty_db_cursor, PATH):
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    shortcuts.delete(args=DELETE_ARGS, datapath=PATH)
    selection = empty_db_cursor.execute(
        '''SELECT * FROM shortcuts WHERE name = ?''', (DELETE_ARGS[0], ))
    assert selection.fetchall() == []


def test_delete_many_shortcuts(empty_db_cursor, PATH):
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=PATH)
    shortcuts.delete(args=DELETE_MANY_ARGS, datapath=PATH)
    for name in DELETE_MANY_ARGS:
        selection = empty_db_cursor.execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (name, ))
        assert selection.fetchall() == []


def test_show_shortcut(empty_db_cursor, PATH):
    destinations = ', '.join([DESTINATION, ANOTHER_DESTINATION])
    expected_output = outputs.show_msg(NAME, SOURCE, destinations)
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.show(args=SHOW_ARGS, datapath=PATH)
        assert mock_output.getvalue().rstrip() == expected_output


def test_showall(empty_db_cursor, PATH):
    expected_output = outputs.showall_msg([NAME, ANOTHER_NAME])
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.showall(args=SHOWALL_ARGS, datapath=PATH)
        assert mock_output.getvalue().rstrip() == expected_output


def test_clear(mock_fields_db):
    expected_output = outputs.clear_msg()
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.clear(args=['clear'], datapath=mock_fields_db)
        with pytest.raises(sqlite3.OperationalError) as e:
            connection = sqlite3.connect(mock_fields_db)
            cursor = connection.cursor()
            selection = cursor.execute('SELECT * FROM shortcuts')
            assert 'no such table: shortcuts' == e.exconly()
        assert mock_output.getvalue().rstrip() == expected_output