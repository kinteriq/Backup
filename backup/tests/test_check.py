# TODO add all commands tests
import pytest
import os
import sqlite3

from backup import check
from .fixtures import PATH, SHORTCUT_NAMES

COMMANDS = ('create', 'delete', 'show')

INVALID_SHORTCUTS = check.CommandLine(datapath=PATH,
                                      arguments=['wrong1', 'wrong2', 'wrong3'],
                                      all_commands=COMMANDS)

BACKUP_ARGS = check.CommandLine(datapath=PATH,
                                arguments=SHORTCUT_NAMES,
                                all_commands=COMMANDS)

INVALID_CMD = check.CommandLine(datapath=PATH,
                                arguments=['messed', 'up'],
                                all_commands=COMMANDS)

INVALID_CMD_ARGS = check.CommandLine(datapath=PATH,
                                     arguments=['showall', 'wrong_name'],
                                     all_commands=COMMANDS)

VALID_CMD = check.CommandLine(
    datapath=PATH,
    arguments=['create', 'NAME', 'from/path', 'to/path'],
    all_commands=COMMANDS)

EMPTY_CMD = check.CommandLine(datapath=PATH,
                              arguments=[],
                              all_commands=COMMANDS)

SHORTCUT_EXISTS_CMD = check.CommandLine(
    datapath=PATH,
    arguments=['create', SHORTCUT_NAMES[0], 'from/path', 'to/path'],
    all_commands=COMMANDS)


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
    with pytest.raises(SystemExit):
        EMPTY_CMD.complete()


def test_check_invalid_shortcuts():
    with pytest.raises(SystemExit):
        INVALID_SHORTCUTS.complete()


def test_check_valid_backup_args():
    """
    If all shortcuts are valid - returns a tuple with valid args,
        where the first arg is None, and the rest - shortcut names.
    """
    assert len(BACKUP_ARGS.complete()) >= 2


def test_check_invalid_command():
    with pytest.raises(SystemExit):
        INVALID_CMD.complete()


def test_created_shortcut_exists():
    with pytest.raises(SystemExit):
        SHORTCUT_EXISTS_CMD.complete()


def test_invalid_command_args():
    with pytest.raises(SystemExit):
        INVALID_CMD_ARGS.complete()


def test_valid_command():
    """
    Test a function returns a non-empty tuple upon receiving a valid command
    """
    assert len(VALID_CMD.complete()) >= 1


def test_wrong_dir_path():
    with pytest.raises(SystemExit):
        check.dir_path('/test_backup_wrong_filepath/')
