from io import StringIO
import os
import pytest
import sqlite3
from unittest import mock

import shortcuts
import outputs
from constants import SHORTCUT_NAMES, DB


CREATE_ARGS = [SHORTCUT_NAMES[0], DB['source'], 
               DB['destination'], DB['another_destination']]

ANOTHER_CREATE_ARGS = [SHORTCUT_NAMES[1], DB['source'], 
                       DB['destination']]


def test_wrong_path_name(empty_db_cursor, DB_PATH):
    with pytest.raises(SystemExit) as e:
        shortcuts.create(args=[SHORTCUT_NAMES[0], 'wrong_path'],
                         datapath=DB_PATH)
    assert 'Directory does not exist' in e.exconly()


def test_shortcut_is_created(empty_db_cursor, DB_PATH):
    expected_result = tuple(CREATE_ARGS[:2] + [', '.join(CREATE_ARGS[2:])])
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    selection = empty_db_cursor.execute('''SELECT * FROM shortcuts''')
    for row in selection:
        assert expected_result == row


def test_update_shortcuts(monkeypatch, empty_db_cursor, DB_PATH):
    expected_output = outputs.update_msg(updated_lst=SHORTCUT_NAMES)
    expected_db_change = [tuple(CREATE_ARGS[1:]),
                          tuple(ANOTHER_CREATE_ARGS[1:])]
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=DB_PATH)

    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        with mock.patch('builtins.input', side_effect=[
                '', DB['another_destination'], '', DB['destination']]):
            shortcuts.update(args=SHORTCUT_NAMES, datapath=DB_PATH)
    assert mock_output.getvalue().rstrip().endswith(expected_output)
    
    selection = empty_db_cursor.execute('''SELECT * FROM shortcuts''')
    for row in selection:
        assert row[1:] in expected_db_change


def test_delete_shortcut(empty_db_cursor, DB_PATH):
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    shortcuts.delete(args=[CREATE_ARGS[0]],
                     datapath=DB_PATH)
    selection = empty_db_cursor.execute(
        '''SELECT * FROM shortcuts WHERE name = ?''', (CREATE_ARGS[0], ))
    assert selection.fetchall() == []


def test_delete_many_shortcuts(empty_db_cursor, DB_PATH):
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=DB_PATH)
    shortcuts.delete(args=SHORTCUT_NAMES, datapath=DB_PATH)
    for name in SHORTCUT_NAMES:
        selection = empty_db_cursor.execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (name, ))
        assert selection.fetchall() == []


def test_show_shortcut(empty_db_cursor, DB_PATH):
    destinations = ', '.join(CREATE_ARGS[2:])
    expected_output = outputs.show_msg(CREATE_ARGS[0],
        CREATE_ARGS[1], destinations)
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.show(args=[CREATE_ARGS[0]], datapath=DB_PATH)
    assert mock_output.getvalue().rstrip() == expected_output


def test_showall(empty_db_cursor, DB_PATH):
    expected_output = outputs.showall_msg(SHORTCUT_NAMES)
    shortcuts.create(args=CREATE_ARGS, datapath=DB_PATH)
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=DB_PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.showall(args=[], datapath=DB_PATH)
    assert mock_output.getvalue().rstrip() == expected_output


def test_clear(mock_fields_db):
    expected_output = outputs.clear_msg()
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.clear(args=['clear'], datapath=mock_fields_db)
        with pytest.raises(sqlite3.OperationalError) as e:
            connection = sqlite3.connect(mock_fields_db)
            cursor = connection.cursor()
            selection = cursor.execute('SELECT * FROM shortcuts')
        assert 'no such table: shortcuts' in e.exconly()
    assert mock_output.getvalue().rstrip() == expected_output