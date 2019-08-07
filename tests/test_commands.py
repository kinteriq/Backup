import unittest
from unittest.mock import patch

from backup.commands import check_args


test_args_shortcut_name = ['NAME']
test_args_valid_command = ['create', 'NAME', 'from/path', 'to/path']
test_args_invalid_command = ['messed', 'up']


class TestCheckArgs(unittest.TestCase):

    @unittest.skip('WIP')
    def test_got_a_shortcut(self):
        self.assertFalse(check_args(test_args_shortcut_name))

    @unittest.skip('WIP')
    def test_got_valid_command(self):
        self.assertTrue(check_args(test_args_valid_command))

    def test_got_invalid_command(self):
        with self.assertRaises(Exception):
            check_args(test_args_invalid_command)
