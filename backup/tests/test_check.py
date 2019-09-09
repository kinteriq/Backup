# TODO add all commands tests
import pytest
import os
import sqlite3

from backup import check
from .fixtures import PATH, mock_fields_db

SHORTCUT_NAMES = ('TEST_1', 'TEST_2')

COMMANDS = ('create', 'delete', 'show')


def test_check_no_args(mock_fields_db, PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH, arguments=[],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['empty'])


def test_check_invalid_shortcuts(mock_fields_db, PATH):
    args = ['wrong1', 'wrong2', 'wrong3']
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=args,
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_cmd'] + args[0])


def test_check_valid_backup_args(mock_fields_db, PATH):
    """
    If all shortcuts are valid - returns a tuple with valid args,
        where the first arg is None, and the rest - shortcut names.
    """
    result = check.CommandLine(datapath=PATH,
                               arguments=SHORTCUT_NAMES,
                               all_commands=COMMANDS)

    assert len(result.complete()) >= 2


def test_check_invalid_command(mock_fields_db, PATH):
    command = ['messed', 'up']
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=command,
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_cmd'] + command[0])


def test_created_shortcut_exists(mock_fields_db, PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(
            datapath=PATH,
            arguments=['create', SHORTCUT_NAMES[0], '1/path', '2/path'],
            all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['created_shortcut_exists'])


def test_invalid_show_command_args(mock_fields_db, PATH):
    name = 'wrong_name'
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=['show', name],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_shortcut'] + name)


def test_valid_command(mock_fields_db, PATH):
    """
    Test a function returns a non-empty tuple upon receiving a valid command
    """
    result = check.CommandLine(
        datapath=PATH,
        arguments=['create', 'NAME', 'from/path', 'to/path'],
        all_commands=COMMANDS)
    assert len(result.complete()) >= 1


def test_invalid_cmd_args(mock_fields_db, PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=['create', 'name'],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_cmd_args'])


def test_wrong_dir_path(mock_fields_db):
    path = '/test_backup_wrong_filepath/'
    with pytest.raises(SystemExit) as e:
        check.dir_path(path)
    assert e.exconly().endswith(check.MSG['wrong_path'] + path)
