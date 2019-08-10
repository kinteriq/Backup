import pytest
import sys


from .context import backup
from backup.commands import _is_command, execute_command
from backup.error import MSG as message
from .fixtures import mock_data

test_args_shortcut_name = ['NAME']
test_args_valid_command = ['create', 'NAME', 'from/path', 'to/path']
test_args_invalid_command = ['messed', 'up']


class TestCheckArgs():
    def test_got_a_shortcut(self):
        with pytest.raises(SystemExit):
            _is_command(test_args_shortcut_name)

    def test_got_valid_command(self):
        assert _is_command(test_args_valid_command)

    def test_got_invalid_command(self):
        with pytest.raises(SystemExit) as e:
            _is_command(test_args_invalid_command)
        assert message['invalid_cmd'] in e.exconly()

    def test_got_empty_line(self):
        with pytest.raises(SystemExit) as e:
            _is_command([])
        assert message['empty'] in e.exconly()


def test_execute_create_command(monkeypatch, mock_data):
    monkeypatch.setattr(
        sys, 'argv', ['backup.py', 'create', 'NAME', 'from/path', 'to/path'])
    output = execute_command(mock_data)
    assert output == f'Shortcut is created: "NAME".'
