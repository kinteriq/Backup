import pytest
import os

import check
import commands
import outputs
from constants import (SHORTCUT_NAMES, CreateCmd, ShowCmd,
                       VALID_ARGS_WITH_MOCK_DB, ShowallCmd, DeleteCmd,
                       UpdateCmd, ClearCmd)


COMMANDS = commands.COMMANDS


INVALID_WITH_MOCK_DB = [
    (ShowCmd(name='wr0ng').args()[1:], 'invalid_shortcut', 'wr0ng'),
    (CreateCmd().args()[1:], 'created_shortcut_exists', None),
    (DeleteCmd(name='wr0ng').args()[1:], 'no_such_shortcut_saved', 'wr0ng'),
    (UpdateCmd(name='wr0ng').args()[1:], 'no_such_shortcut_saved', 'wr0ng'),
]


INVALID_WITH_EMPTY_DB = [
    (CreateCmd(cmd='wr0ng').args()[1:], 'invalid_cmd', 'wr0ng'),
    (ShowallCmd().args()[1:], 'no_data', None),
    (CreateCmd().args()[1:3], 'invalid_cmd_args', None),

]


def valid_cmd(db, args):
    return check.CommandLine(datapath=db,
                             arguments=args,
                             all_commands=COMMANDS)

    
def raise_exit_cmd(db, args):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=db,
                          arguments=args,
                          all_commands=COMMANDS).complete()
    return e


@pytest.mark.commands
@pytest.mark.check_complete
def test_check_documentation_output(empty_db_cursor, DB_PATH):
    e = raise_exit_cmd(DB_PATH, [])
    assert outputs.COMMANDS_INFO.rstrip() in e.exconly(),\
        'Missing documentation output'


@pytest.mark.commands
@pytest.mark.check_complete
def test_valid_create_command(empty_db_cursor, DB_PATH):
    """
    Test a function returns a tuple with valid args
        upon receiving a valid command
    """
    result = valid_cmd(DB_PATH, CreateCmd().args()[1:])
    assert result.complete() == tuple(CreateCmd().args()[1:]),\
        'Create cmd complete check returned incorrect args'


@pytest.mark.commands
@pytest.mark.check_complete
@pytest.mark.parametrize('args', VALID_ARGS_WITH_MOCK_DB)
def test_valid_commands(mock_fields_db, args):
    """
    Test a function returns a tuple with valid args
        upon receiving a valid command
    """
    result = valid_cmd(mock_fields_db, args[1:])
    assert result.complete() == tuple(args[1:]),\
        'Complete check returned incorrect args'


@pytest.mark.commands
@pytest.mark.check_complete
def test_check_valid_backup_args(mock_fields_db):
    """
    If all shortcuts are valid - returns a tuple with valid args,
        where the first arg is None, and the rest - shortcut names.
    """
    result = valid_cmd(mock_fields_db, SHORTCUT_NAMES)
    assert result.complete() == (None, *SHORTCUT_NAMES),\
        'Runbackup check returned incorrect args'


@pytest.mark.commands
@pytest.mark.check_complete
@pytest.mark.parametrize('args, error, param', INVALID_WITH_MOCK_DB)
def test_invalid_commands(mock_fields_db, args, error, param):
    e = raise_exit_cmd(mock_fields_db, args)
    try:
        assert e.exconly().endswith(
            outputs.ERROR_MSG[error](param)), f'Missing {error} error message'
    except TypeError:
        assert e.exconly().endswith(
            outputs.ERROR_MSG[error]), f'Missing {error} error message'


@pytest.mark.commands
@pytest.mark.check_complete
@pytest.mark.parametrize('args, error, param', INVALID_WITH_EMPTY_DB)
def test_invalid_commands(empty_db_cursor, DB_PATH, args, error, param):
    e = raise_exit_cmd(DB_PATH, args)
    try:
        assert e.exconly().endswith(
            outputs.ERROR_MSG[error](param)), f'Missing {error} error message'
    except TypeError:
        assert e.exconly().endswith(
            outputs.ERROR_MSG[error]), f'Missing {error} error message'


@pytest.mark.commands
@pytest.mark.check_complete
def test_try_showall_with_no_db(DB_PATH):
    e = raise_exit_cmd(DB_PATH, ShowallCmd().args()[1:])
    assert e.exconly().endswith(outputs.ERROR_MSG['no_data']),\
        'Missing no_data error message'


@pytest.mark.check_path
def test_wrong_path():
    path = '/test_backup_wrong_filepath/'
    with pytest.raises(SystemExit) as e:
        check.Path.single(path)
    assert e.exconly().endswith(outputs.ERROR_MSG['wrong_path'](path)),\
        'Missing wrong_path error message'


@pytest.mark.check_path
def test_correct_path():
    path = os.getcwd()
    assert check.Path.single(path) == path,\
        'check.Path.single returned incorrect path'


@pytest.mark.check_path
def test_auto_expand_path():
    path = '~/'
    assert check.Path.single(path) == os.path.expanduser('~/'),\
        'Path with "~" was not expanded correctrly'
