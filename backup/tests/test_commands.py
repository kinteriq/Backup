import pytest
import sys

from .context import backup
from backup.commands import is_command, execute_command
from backup.error import MSG as message
from .fixtures import mock_data

test_shortcut = 'NAME'
test_args_shortcut_name = [test_shortcut]
test_args_valid_command = ['create', test_shortcut, 'from/path', 'to/path']
test_args_invalid_command = ['messed', 'up']
test_args_from_cmd = [
    'backup.py', 'create', test_shortcut, 'from/path', 'to/path'
]


class TestCheckArgs():
    def test_got_a_shortcut(self):
        data = dict()
        data[test_shortcut] = 'testing'
        with pytest.raises(SystemExit):
            is_command(test_args_shortcut_name, data)

    def test_got_valid_command(self):
        assert is_command(test_args_valid_command, {})

    def test_got_invalid_command(self):
        with pytest.raises(SystemExit) as e:
            is_command(test_args_invalid_command, {})
        assert message['invalid_cmd'] in e.exconly()

    def test_got_empty_line(self):
        with pytest.raises(SystemExit) as e:
            is_command([], {})
        assert message['empty'] in e.exconly()


def test_execute_create_command(monkeypatch, mock_data):
    monkeypatch.setattr(sys, 'argv', test_args_from_cmd)
    output = execute_command(mock_data)
    assert output == f'Shortcut is created: "{test_shortcut}".'
