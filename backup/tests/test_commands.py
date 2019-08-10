import pytest
import sys

from .context import backup
from backup.commands import read_from_command_line, execute_command
from backup.error import MSG as error_message
from .fixtures import mock_data

test_shortcut = 'NAME'
test_args_shortcut_name = ['backup.py', test_shortcut]
test_args_valid_command = [
    'backup.py', 'create', test_shortcut, 'from/path', 'to/path'
]
test_args_invalid_command = ['backup.py', 'messed', 'up']
test_args_showall_command = ['backup.py', 'showall']


class TestReadFromCommandLine():
    def test_got_a_shortcut(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', test_args_shortcut_name)
        data = dict()
        data[test_shortcut] = 'testing'
        with pytest.raises(SystemExit):
            read_from_command_line(data)

    def test_got_valid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', test_args_valid_command)
        assert read_from_command_line({})

    def test_got_invalid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', test_args_invalid_command)
        with pytest.raises(SystemExit) as e:
            read_from_command_line({})
        assert error_message['invalid_cmd'] in e.exconly()

    def test_got_empty_line(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', [])
        with pytest.raises(SystemExit) as e:
            read_from_command_line({})
        assert error_message['empty'] in e.exconly()

    def test_got_showall_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', test_args_showall_command)
        data = dict()
        data[test_shortcut] = 'testing'
        with pytest.raises(SystemExit) as e:
            read_from_command_line(data)
        assert test_shortcut in e.exconly()


def test_execute_create_command(mock_data):
    test_shortcut = test_args_valid_command[2]
    command, *params = test_args_valid_command[1:]
    output = execute_command(data=mock_data, command=command, params=params)
    assert output == f'Shortcut is created: "{test_shortcut}".'
