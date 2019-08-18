import pytest
import sys

from .context import backup
from backup.commands import read_from_command_line, execute_command
from backup.check import MSG as error_message
from .fixtures import mock_data

EMPTY_ARGS = []

NO_DATA = {}

SHORTCUT_NAMES = ['first', 'second', 'third']

INVALID_CMD_ARGS = ['backup.py', 'messed', 'up']

SHOWALL_ARGS = ['backup.py', 'showall']

BACKUP_ARGS = ['backup.py'] + SHORTCUT_NAMES

VALID_CMD_ARGS = ['backup.py', 'create', 'NAME', 'from/path', 'to/path']


class TestReadFromCommandLine():
    def test_got_empty_line(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', EMPTY_ARGS)
        with pytest.raises(SystemExit) as e:
            read_from_command_line(data=NO_DATA)
        assert error_message['empty'] in e.exconly()

    def test_got_invalid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', INVALID_CMD_ARGS)
        with pytest.raises(SystemExit) as e:
            read_from_command_line(NO_DATA)
        assert error_message['invalid_cmd'] in e.exconly()

    def test_got_showall_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', SHOWALL_ARGS)
        data = dict()
        data['first'] = 'testing'
        data['second'] = 'another test'
        assert read_from_command_line(data=data)

    def test_got_a_shortcut(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', BACKUP_ARGS)
        data = dict()
        for name in SHORTCUT_NAMES:
            data[name] = '_'
        command, *params = read_from_command_line(data=data)
        print(command, params)
        assert (command, params) == (None, BACKUP_ARGS[1:])

    def test_got_valid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', VALID_CMD_ARGS)
        assert read_from_command_line(data=NO_DATA)


def test_execute_create_command(mock_data):
    shortcut = VALID_CMD_ARGS[2]
    command, *params = VALID_CMD_ARGS[1:]
    expected_output = f'Shortcut is created: {shortcut}.'
    output, _ = execute_command(command=command, params=params, data=mock_data)
    assert output == expected_output
