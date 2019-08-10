import os
import sys
import json
import unittest
from unittest.mock import patch

from .context import backup
from backup.commands import execute_command

CREATE_ARGS = [
    'backup.py', 'create', 'test', 'wrong/pathfrom', 'path/to_1', 'path/to_2'
]

SHOW_ARGS = ['backup.py', 'show', CREATE_ARGS[2]]

UPDATE_ARGS = ['backup.py', 'update', CREATE_ARGS[2]]

BACKUP_ARGS = ['backup.py', CREATE_ARGS[2]]


def patched_execute_command(data, args):
    with patch.object(sys, 'argv', args):
        output = execute_command(data)
        return output


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        with open('shortcuts_test.json', 'w') as file:
            file.write(json.dumps({}))
        with open('shortcuts_test.json', 'r') as file:
            self.data = json.load(file)
        self.shortcut = CREATE_ARGS[2]

    def tearDown(self):
        os.remove('shortcuts_test.json')

    # User creates a shortcut and sees the program's output
    def test_receive_create_command(self):
        expected_output = f'Shortcut is created: "{self.shortcut}".'
        output = patched_execute_command(self.data, CREATE_ARGS)
        self.assertEqual(output, expected_output)

    # Checks that the shortcut was saved by entering 'show {shortcut}' command
    def test_receive_show_command(self):
        path_from = CREATE_ARGS[3]
        paths_to = CREATE_ARGS[4:]
        expected_output = f'{self.shortcut}:\n' +\
            str(
                {
                    'source': path_from,
                    'destination': paths_to
                }
            )
        patched_execute_command(self.data, CREATE_ARGS)
        output = patched_execute_command(self.data, SHOW_ARGS)
        self.assertEqual(output, expected_output)

    # Sees that the source path is wrong;
    #   Changes the source path
    user_input = ['changed/path', '']

    @patch('builtins.input', side_effect=user_input)
    def test_receive_update_command(self, user_input):
        expected_output = 'Updated successfully.'
        patched_execute_command(self.data, CREATE_ARGS)
        output = patched_execute_command(self.data, UPDATE_ARGS)
        self.assertEqual(output, expected_output)

    # Does a backup using the saved shortcut
    def test_backup(self):
        patched_execute_command(self.data, CREATE_ARGS)
        with self.assertRaisesRegex(SystemExit, 'BACKUP IS FINISHED'):
            patched_execute_command(self.data, BACKUP_ARGS)


if __name__ == '__main__':
    unittest.main()
