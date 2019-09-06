# TODO add all commands tests
import pytest
import os
import sqlite3

from backup import check
from .fixtures import PATH

SHORTCUT_NAMES = ('TEST_1', 'TEST_2')

COMMANDS = ('create', 'delete', 'show')


def setup_module():
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


def teardown_module():
    os.remove(PATH)


def test_check_no_args():
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH, arguments=[],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['empty'])


def test_check_invalid_shortcuts():
    args = ['wrong1', 'wrong2', 'wrong3']
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=args,
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_cmd'] + args[0])


def test_check_valid_backup_args():
    """
    If all shortcuts are valid - returns a tuple with valid args,
        where the first arg is None, and the rest - shortcut names.
    """
    result = check.CommandLine(datapath=PATH,
                               arguments=SHORTCUT_NAMES,
                               all_commands=COMMANDS)

    assert len(result.complete()) >= 2


def test_check_invalid_command():
    command = ['messed', 'up']
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=command,
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_cmd'] + command[0])


def test_created_shortcut_exists():
    with pytest.raises(SystemExit) as e:
        check.CommandLine(
            datapath=PATH,
            arguments=['create', SHORTCUT_NAMES[0], '1/path', '2/path'],
            all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['created_shortcut_exists'])


def test_invalid_show_command_args():
    name = 'wrong_name'
    with pytest.raises(SystemExit) as e:
        check.CommandLine(datapath=PATH,
                          arguments=['show', name],
                          all_commands=COMMANDS).complete()
    assert e.exconly().endswith(check.MSG['invalid_shortcut'] + name)


def test_valid_command():
    """
    Test a function returns a non-empty tuple upon receiving a valid command
    """
    result = check.CommandLine(
        datapath=PATH,
        arguments=['create', 'NAME', 'from/path', 'to/path'],
        all_commands=COMMANDS)
    assert len(result.complete()) >= 1


def test_wrong_dir_path():
    path = '/test_backup_wrong_filepath/'
    with pytest.raises(SystemExit) as e:
        check.dir_path(path)
    assert e.exconly().endswith(check.MSG['wrong_path'] + path)
