import pytest
import os

import check
import commands
import outputs
from constants import SHORTCUT_NAMES, CreateCmd, ShowCmd, ShowallCmd


# TODO add all commands tests
COMMANDS = commands.COMMANDS


@pytest.mark.runbackup
@pytest.mark.check_complete
def test_check_valid_backup_args(mock_fields_db, DB_PATH):
    """
    If all shortcuts are valid - returns a tuple with valid args,
        where the first arg is None, and the rest - shortcut names.
    """
    result = check.CommandLine(datapath=DB_PATH,
                               arguments=SHORTCUT_NAMES,
                               all_commands=COMMANDS)
    assert result.complete() == (None, *SHORTCUT_NAMES),\
        'Complete check returned incorrect args'


@pytest.mark.create
@pytest.mark.check_complete
def test_valid_command(empty_db_cursor, DB_PATH):
    """
    Test a function returns a tuple with valid args
        upon receiving a valid command
    """
    result = check.CommandLine(datapath=DB_PATH,
                               arguments=CreateCmd().args()[1:],
                               all_commands=COMMANDS)
    assert result.complete() == tuple(CreateCmd().args()[1:]),\
        'Complete check returned incorrect args'


@pytest.mark.check_complete
def test_check_invalid_cmd_name(empty_db_cursor, DB_PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=DB_PATH,
                          arguments=CreateCmd(cmd='wr0ng').args()[1:],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(outputs.ERROR_MSG['invalid_cmd']('wr0ng')),\
        'Missing invalid_cmd error message'


@pytest.mark.show
@pytest.mark.check_complete
def test_invalid_show_command_shortcut(mock_fields_db):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=mock_fields_db,
                          arguments= ShowCmd(name='wr0ng').args()[1:],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(
        outputs.ERROR_MSG['invalid_shortcut']('wr0ng')),\
        'Missing invalid_shortcut error message'


@pytest.mark.showall
@pytest.mark.check_complete
def test_try_showall_with_no_db(DB_PATH):
    with pytest.raises(SystemExit) as e:
        result = check.CommandLine(datapath=DB_PATH,
                                   arguments=ShowallCmd().args()[1:],
                                   all_commands=COMMANDS).complete()
    assert e.exconly().endswith(outputs.ERROR_MSG['no_data']),\
        'Missing no_data error message'


@pytest.mark.showall
@pytest.mark.check_complete
def test_try_showall_with_no_shortcuts_saved(empty_db_cursor, DB_PATH):
    with pytest.raises(SystemExit) as e:
        result = check.CommandLine(datapath=DB_PATH,
                                   arguments=['showall'],
                                   all_commands=COMMANDS).complete()
    assert e.exconly().endswith(outputs.ERROR_MSG['no_data']),\
        'Missing no_data error message'


@pytest.mark.doc
@pytest.mark.check_complete
def test_check_documentation_output(empty_db_cursor, DB_PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=DB_PATH,
                          arguments=[],
                          all_commands=COMMANDS).complete()
    assert outputs.COMMANDS_INFO.rstrip() in e.exconly(),\
        'Missing documentation output'


@pytest.mark.create
@pytest.mark.check_complete
def test_not_enough_create_command_args(empty_db_cursor, DB_PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=DB_PATH,
                          arguments=CreateCmd().args()[1:3],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(
        outputs.ERROR_MSG['invalid_cmd_args']),\
        'Missing invalid_cmd_args error message'


@pytest.mark.create
@pytest.mark.check_complete
def test_created_shortcut_exists(mock_fields_db, DB_PATH):
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=DB_PATH,
                          arguments=CreateCmd().args()[1:],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(
        outputs.ERROR_MSG['created_shortcut_exists']),\
        'Missing created_shortcut_exists error message'


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
