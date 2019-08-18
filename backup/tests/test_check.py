# TODO add all commands tests
import pytest

from backup import check

DATA = {
    'TEST1': {},
    'TEST2': {},
    'TEST3': {},
}

commands = ('create', 'delete', 'show')

INVALID_SHORTCUTS = check.CommandLine(data=DATA,
                                      arguments=['wrong1', 'wrong2', 'wrong3'],
                                      all_commands=commands)

BACKUP_ARGS = check.CommandLine(data=DATA,
                                arguments=list(DATA.keys()),
                                all_commands=commands)

INVALID_CMD = check.CommandLine(data=DATA,
                                arguments=['messed', 'up'],
                                all_commands=commands)

INVALID_CMD_ARGS = check.CommandLine(data=DATA,
                                     arguments=['showall', 'up'],
                                     all_commands=commands)

VALID_CMD = check.CommandLine(
    data={},
    arguments=['create', 'TEST1', 'from/path', 'to/path'],
    all_commands=commands)

EMPTY_CMD = check.CommandLine(data=DATA, arguments=[], all_commands=commands)

SHORTCUT_EXISTS_CMD = check.CommandLine(
    data=DATA,
    arguments=['create', 'TEST1', 'from/path', 'to/path'],
    all_commands=commands)


def test_check_no_args():
    with pytest.raises(SystemExit):
        EMPTY_CMD.complete()


def test_check_invalid_shortcuts():
    with pytest.raises(SystemExit):
        INVALID_SHORTCUTS.complete()


def test_check_valid_backup_args():
    """
    If all shortcuts are valid - returns a tuple with runbackup args,
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
    Tests function which returns tuple upon receiving a valid command
    """
    assert len(VALID_CMD.complete()) >= 1
