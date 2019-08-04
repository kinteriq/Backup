import sys
import unittest
from unittest.mock import patch

from backup import receive_command, execute_command


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        self.test_args = [
            'backup.py',
            'create',
            'shortcut_name',
            'path_from',
            'path_to_1',
            'path_to_2'
        ]
        self.paths_to = set(self.test_args[4:])
        with patch.object(sys, 'argv', self.test_args):
            self.command_line = receive_command()

    # enter 'create' command into command line
    def test_receive_create_command(self):
        should_receive = tuple(self.test_args[1:4] + [ self.paths_to ])
        self.assertEqual(self.command_line, should_receive)

    # see '"{name}" shortcut is created.' in the output
    def test_command_is_executed_correctly(self):
        shortcut = self.command_line[1]
        result = execute_command(self.command_line)
        expected_result = f'"{shortcut}" shortcut is created.'
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
