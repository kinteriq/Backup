import sys
import unittest
from unittest.mock import patch

from backup import receive_command, execute_command


CREATE_ARGS = [
    'backup.py',
    'create',
    'test',
    'path/from',
    'path/to_1',
    'path/to_2'
]

SHOW_ARGS = [
    'backup.py',
    'show',
    'test'
]


def receive_cmd(test_args):
    with patch.object(sys, 'argv', test_args):
        command_line = receive_command()
    return command_line


class TestCommandLine(unittest.TestCase):
    '''
    1. User creates "test" shortcut;
    2. Checks "test" shortcut was saved;
    3. ...
    '''
    def setUp(self):
        # create a shortcut from command line
        self.create_command = receive_cmd(CREATE_ARGS)

    # program received 'create' command
    def test_receive_create_command(self):
        command, arguments = CREATE_ARGS[1], CREATE_ARGS[2:]
        should_receive = tuple([command, arguments])
        self.assertEqual(self.create_command, should_receive)

    # see that shortcut was created from the output
    def test_command_is_executed_correctly(self):
        result = execute_command(self.create_command)
        shortcut = CREATE_ARGS[2]
        expected_result = f'Shortcut is created: "{shortcut}".'
        self.assertEqual(result, expected_result)

    # see the result of saving a shortcut by
    # entering 'show test' in the command line
    def test_receive_show_command(self):
        show_command = receive_cmd(SHOW_ARGS)
        result = execute_command(show_command)
        shortcut = CREATE_ARGS[2]
        path_from = CREATE_ARGS[3]
        paths_to = CREATE_ARGS[4:]
        expected_result = [
            f'{shortcut}:\n' +
                str(
                {
                    'original': path_from,
                    'destination': paths_to
                }
            )
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
