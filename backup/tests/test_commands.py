import pytest

from .context import backup
from backup.commands import check_args

test_args_shortcut_name = ['NAME']
test_args_valid_command = ['create', 'NAME', 'from/path', 'to/path']
test_args_invalid_command = ['messed', 'up']


class TestCheckArgs():
    def test_got_a_shortcut(self):
        assert not check_args(test_args_shortcut_name)

    def test_got_valid_command(self):
        assert check_args(test_args_valid_command)

    def test_got_invalid_command(self):
        with pytest.raises(SystemExit):
            check_args(test_args_invalid_command)

    def test_got_empty_line(self):
        with pytest.raises(SystemExit):
            check_args([])
