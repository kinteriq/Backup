from io import StringIO
import os
import pytest
import sqlite3
from unittest import mock

import shortcuts
import outputs
from constants import CREATE_1, CREATE_2
from commands import COMMANDS


def execute(cmd, args, db):
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        COMMANDS[cmd](args=args, datapath=db)
    return mock_output.getvalue().rstrip()


@pytest.mark.commands
@pytest.mark.create
def test_shortcut_is_created(empty_db_cursor, DB_PATH):
    expected_result = (CREATE_1.name, CREATE_1.source,
                       ', '.join(CREATE_1.destinations))
    output = execute('create', CREATE_1.args()[2:], DB_PATH)

    selection = empty_db_cursor.execute('''SELECT * FROM shortcuts''')
    assert selection.fetchone() == expected_result,\
        'Shortcut was not created'

    assert output == outputs.create_msg(CREATE_1.name),\
        'Incorrect output for "create" cmd'


@pytest.mark.commands
@pytest.mark.update
def test_update_wrong_source(monkeypatch, mock_fields_db, mock_fields_db_cursor):
    with pytest.raises(SystemExit) as e:
        with mock.patch('builtins.input', side_effect=['wr0ng', '']):
            execute('update', [CREATE_1.name], mock_fields_db)

    assert e.value.args[0] == outputs.ERROR_MSG['wrong_path']('wr0ng'),\
        'Incorrect output for non-existent updated source path'


@pytest.mark.commands
@pytest.mark.update
def test_update_wrong_destination(monkeypatch, mock_fields_db, mock_fields_db_cursor):
    with pytest.raises(SystemExit) as e:
        with mock.patch('builtins.input', side_effect=['', 'wr0ng/']):
            execute('update', [CREATE_1.name], mock_fields_db)

    assert e.value.args[0] == outputs.ERROR_MSG['wrong_path']('wr0ng'),\
        'Incorrect output for non-existent updated destination path'


@pytest.mark.commands
@pytest.mark.update
def test_update_one_shortcut(monkeypatch, mock_fields_db, mock_fields_db_cursor):
    expected_output = outputs.update_msg(updated_lst=[CREATE_1.name])
    expected_db_change = [
        (CREATE_1.name, CREATE_1.source, ', '.join(CREATE_2.destinations)),
        (CREATE_2.name, CREATE_2.source, ', '.join(CREATE_2.destinations))
    ]

    with mock.patch('builtins.input', side_effect=[
        '',
        ', '.join(CREATE_2.destinations)
    ]):
        output = execute('update', [CREATE_1.name], mock_fields_db)
    
    selection = mock_fields_db_cursor.execute('''SELECT * FROM shortcuts''')
    assert selection.fetchall() == expected_db_change,\
        'Shortcut was not updated'
    
    assert output.endswith(expected_output),\
        'Incorrect output for "update" cmd'


@pytest.mark.commands
@pytest.mark.update
def test_update_many_shortcuts(monkeypatch, mock_fields_db, mock_fields_db_cursor):
    expected_output = outputs.update_msg(
        updated_lst=[CREATE_1.name, CREATE_2.name])
    expected_db_change = [
        (CREATE_1.name, CREATE_1.source, ', '.join(CREATE_2.destinations)),
        (CREATE_2.name, CREATE_2.source, ', '.join(CREATE_1.destinations))
    ]

    with mock.patch('builtins.input', side_effect=[
        '',
        ', '.join(CREATE_2.destinations),
        '',
        ', '.join(CREATE_1.destinations)
    ]):
        output = execute('update', [CREATE_1.name, CREATE_2.name],
                         mock_fields_db)
    
    selection = mock_fields_db_cursor.execute('''SELECT * FROM shortcuts''')
    assert selection.fetchall() == expected_db_change,\
        'Shortcuts were not updated'
    
    assert output.endswith(expected_output),\
        'Incorrect output for "update" cmd'


@pytest.mark.commands
@pytest.mark.delete
def test_delete_one_shortcut_out_of_many(mock_fields_db, mock_fields_db_cursor):
    output = execute('delete', [CREATE_1.name], mock_fields_db)

    selection = mock_fields_db_cursor.execute('''SELECT * FROM shortcuts''')
    assert selection.fetchall() == [tuple(CREATE_2.args()[2:])],\
        'Both shortcuts were deleted istead of one'
    
    assert output == outputs.delete_msg([CREATE_1.name]),\
        'Incorrect output for "delete" cmd'


@pytest.mark.commands
@pytest.mark.delete
def test_delete_all_shortcuts(mock_fields_db, mock_fields_db_cursor):
    args = [CREATE_1.name, CREATE_2.name]
    output = execute('delete', args, mock_fields_db)

    for name in args:
        selection = mock_fields_db_cursor.execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (name, ))
        assert selection.fetchall() == [],\
            'One or more shortcuts was not deleted'
    
    assert output == outputs.delete_msg(args),\
        'Incorrect output for "delete" cmd'


@pytest.mark.commands
@pytest.mark.show
def test_show_shortcut(mock_fields_db):
    expected = outputs.show_msg(CREATE_1.name, CREATE_1.source,
                                ', '.join(CREATE_1.destinations))
    output = execute('show', [CREATE_1.name], mock_fields_db)
    assert output == expected,\
        'Incorrect output for "show" cmd'


@pytest.mark.commands
@pytest.mark.showall
def test_showall(mock_fields_db):
    expected = outputs.showall_msg([CREATE_1.name, CREATE_2.name])
    output = execute('showall', [], mock_fields_db)
    assert output == expected,\
        'Incorrect output for "showall" cmd'


@pytest.mark.commands
@pytest.mark.clear
@pytest.mark.db_content
def test_clear(mock_fields_db, mock_fields_db_cursor):
    output = execute('clear', CREATE_1.args()[1:], mock_fields_db)
    
    with pytest.raises(sqlite3.OperationalError) as e:
        selection = mock_fields_db_cursor.execute('SELECT * FROM shortcuts')
    assert e.value.args[0] == 'no such table: shortcuts',\
        'Table "shortcuts" was not deleted'
    
    assert output == outputs.clear_msg(),\
        'Incorrect output for "clear" cmd'
    