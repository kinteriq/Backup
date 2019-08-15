import os
import sys
import json
import unittest
from unittest.mock import patch

from .context import backup
from backup.commands import read_from_command_line, execute_command

NO_ARGS = ['backup.py']

CREATE_ARGS = [
    'backup.py', 'create', 'test', 'wrong/pathfrom', 'path/to_1', 'path/to_2'
]

WRONG_CREATE_COMMAND_ARGS = [
    'backup.py', 'crete', 'test', 'wrong/pathfrom', 'path/to_1', 'path/to_2'
]

SHOW_ARGS = ['backup.py', 'show', CREATE_ARGS[2]]

UPDATE_ARGS = ['backup.py', 'update', CREATE_ARGS[2]]

ANOTHER_CREATE_ARGS = [
    'backup.py', 'create', 'test_2', 'pathfrom', 'path/to_1', 'path/to_2'
]

SHOWALL_ARGS = ['backup.py', 'showall']

WRONG_SHORTCUT_ARGS = ['backup.py', str(CREATE_ARGS[2]) + 'wrong']

BACKUP_ARGS = ['backup.py', CREATE_ARGS[2]]

DELETE_ARGS = ['backup.py', 'delete', CREATE_ARGS[2]]


def patched_read_from_command_line(args, data):
    with patch.object(sys, 'argv', args):
        params = read_from_command_line(data)
        return params


def mock_create_command(data, args=CREATE_ARGS):
    command, *params = patched_read_from_command_line(args=args, data=data)
    output, _ = execute_command(command=command, params=params, data=data)
    return output


def execution(args, data):
    """
    creates some mock data
    executes particular command
    returns result of execution
    """
    mock_create_command(data=data)
    command, *params = patched_read_from_command_line(args=args, data=data)
    output, _ = execute_command(command=command, params=params, data=data)
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

    # User enters empty command
    def test_receive_empty_command(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=NO_ARGS, data=self.data)

    # User tries creating a shortcut but misspells 'create'
    def test_receive_invalid_command(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=WRONG_CREATE_COMMAND_ARGS,
                                           data=self.data)

    # User creates a shortcut and sees the program's output
    def test_receive_create_command(self):
        expected_output = f'Shortcut is created: {self.shortcut}.'
        output = mock_create_command(data=self.data)
        self.assertEqual(output, expected_output)

    # Checks that the shortcut was saved by entering 'show {shortcut}' command
    def test_receive_show_command(self):
        path_from = CREATE_ARGS[3]
        paths_to = CREATE_ARGS[4:]
        expected_output = (f'\n{self.shortcut}:\n  ' +
                           str({
                               'source': path_from,
                               'destination': paths_to
                           }) + '\n')
        output = execution(args=SHOW_ARGS, data=self.data)
        self.assertEqual(output, expected_output)

    # Sees that the source path is wrong;
    #   Changes the source path
    user_input = ['changed/path', '']

    @patch('builtins.input', side_effect=user_input)
    def test_receive_update_command(self, user_input):
        expected_output = 'Updated successfully.'
        output = execution(args=UPDATE_ARGS, data=self.data)
        self.assertEqual(output, expected_output)

    # User creates another shortcut and checks that they are both saved
    # with 'showall' command
    def test_receive_showall_command(self):
        mock_create_command(data=self.data, args=ANOTHER_CREATE_ARGS)
        output = execution(args=SHOWALL_ARGS, data=self.data)
        expected_output = '\n'.join(self.data.keys())
        self.assertEqual(output, expected_output)

    # User tries backing up using the saved shortcut but misspells its name
    def test_receive_invalid_shortcut_name(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=WRONG_SHORTCUT_ARGS,
                                           data=self.data)

    # Enters the correct shortcut's name
    # TODO

    # Decides to delete shortcut from the database
    def test_receive_delete_command(self):
        count = len(DELETE_ARGS[2:])
        deleted_sequence = ', '.join(DELETE_ARGS[2:])
        expected_output = (f'Successfully deleted {count} '
                           f'shortcut(s): {deleted_sequence}.')
        output = execution(args=DELETE_ARGS, data=self.data)
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
