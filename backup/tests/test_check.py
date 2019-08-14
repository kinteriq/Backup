import pytest

from backup.check import (empty, invalid_shortcut_name, invalid_command,
                          shortcut_exists)

INVALID_CMD_ARGS = ['messed', 'up']

VALID_CMD_ARGS = ['create', 'NAME', 'from/path', 'to/path']


def test_check_no_args():
    with pytest.raises(SystemExit):
        empty(arguments=[])


def test_check_there_are_args():
    result = empty(arguments=['some'])
    assert result is None


def test_check_invalid_shortcut_name():
    with pytest.raises(SystemExit):
        invalid_shortcut_name(data={}, arguments=['NAME'])


def test_check_valid_shortcut_name():
    result = invalid_shortcut_name(data={'NAME': 'none'}, arguments=['NAME'])
    assert result is None


def test_check_invalid_command():
    with pytest.raises(SystemExit):
        invalid_command(commands={}, arguments=INVALID_CMD_ARGS)


def test_check_valid_command():
    result = invalid_command(commands={VALID_CMD_ARGS[0]: 'none'},
                             arguments=VALID_CMD_ARGS)
    assert result is None


def test_shortcut_exists():
    with pytest.raises(SystemExit):
        shortcut_exists(data={'NAME': 'none'}, shortcut='NAME')


def test_check_shortcut_does_not_exist():
    result = shortcut_exists(data={}, shortcut='NAME')
    assert result is None
