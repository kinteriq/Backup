import os
import sys
import unittest
from unittest.mock import patch

from file_handler import create_json, read_from
from backup import receive_command, execute_command


CREATE_ARGS= [
    'backup.py', 'create', 'test', 'path/from', 'path/to_1', 'path/to_2'
]

SHOW_ARGS = ['backup.py', 'show', CREATE_ARGS[2]]

UPDATE_ARGS = ['backup.py', 'update', CREATE_ARGS[2]]

BACKUP_ARGS = ['backup.py', CREATE_ARGS[2]]


def receive_cmd(test_args, data):
    with patch.object(sys, 'argv', test_args):
        command_line = receive_command(data)
    return command_line


class TestCommandLine(unittest.TestCase):
    """
    1. User creates a shortcut;
    2. Checks that the shortcut was saved;
    3. Sees that the source path is wrong;
       Changes the source path;
    4. Does a backup using the saved shortcut;
    5. ...
    """
    def setUp(self):
        # create a shortcut from command line
        self.data = create_json('shortcuts_test.json')
        self.create_cmd = receive_cmd(CREATE_ARGS, data=self.data)

    def tearDown(self):
        os.remove('shortcuts_test.json')

    # program receives 'create' command
    def test_receive_create_command(self):
        command, arguments = CREATE_ARGS[1], CREATE_ARGS[2:]
        should_receive = tuple([command, arguments, self.data])
        self.assertEqual(self.create_cmd, should_receive)

    # see the output that the shortcut was created
    def test_create_command_is_executed_correctly(self):
        result = execute_command(self.create_cmd)
        shortcut = CREATE_ARGS[2]
        expected_result = f'Shortcut is created: "{shortcut}".'
        self.assertEqual(result, expected_result)

    # see the result of saving the shortcut by
    # entering 'show' in the command line
    def test_receive_show_command(self):
        execute_command(self.create_cmd)
        show_cmd = receive_cmd(SHOW_ARGS, data=self.data)
        result = execute_command(show_cmd)
        shortcut = CREATE_ARGS[2]
        path_from = CREATE_ARGS[3]
        paths_to = CREATE_ARGS[4:]
        expected_result = f'{shortcut}:\n' +\
            str(
                {
                    'source': path_from,
                    'destination': paths_to
                }
            )
        self.assertEqual(result, expected_result)

    # change the shortcut's path
    user_input = ['change', '']

    @patch('builtins.input', side_effect=user_input)
    def test_receive_update_command(self, user_input):
        execute_command(self.create_cmd)
        update_cmd = receive_cmd(UPDATE_ARGS, data=self.data)
        result = execute_command(update_cmd)
        expected_result = 'Updated successfully.'
        self.assertEqual(result, expected_result)

    def test_backup(self):
        execute_command(self.create_cmd)
        shortcut = CREATE_ARGS[2]
        backup_cmd = receive_cmd(BACKUP_ARGS, data=self.data)
        result = execute_command(backup_cmd)
        expected_result = f'Successfully backed up: {shortcut}.'
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
