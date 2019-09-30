from io import StringIO
import os
import sys
import sqlite3
import shutil
import unittest
from unittest.mock import patch

import outputs
from commands import read_from_command_line, execute_command


PATH = os.path.join(os.getcwd(), 'func_test.db')

SHORTCUT_NAMES = ['TEST_1', 'TEST_2']

_up_level_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))
DB = {
    'name': SHORTCUT_NAMES[0],
    'source': os.path.dirname(__file__),
    'destination': os.path.join(_up_level_dir, 'testBackup1'),
    'another_destination': os.path.join(_up_level_dir, 'testBackup2')
}

CREATE_ARGS = ['backup.py', 'create', SHORTCUT_NAMES[0],
               DB['source'], DB['destination']]

ANOTHER_CREATE_ARGS = [
    'backup.py', 'create', SHORTCUT_NAMES[1], DB['source'],
    DB['destination'], DB['another_destination']
]


def patched_read_from_command_line(args, path):
    with patch.object(sys, 'argv', args):
        valid_args = read_from_command_line(path)
        return valid_args


class TestCommandLine(unittest.TestCase):
    def setUp(self):
        connection = sqlite3.connect(PATH)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE shortcuts
            (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
        connection.commit()
        connection.close()

    def tearDown(self):
        os.remove(PATH)

    # User enters empty command and sees app documentation
    def test_receive_empty_command(self):
        with self.assertRaises(SystemExit) as e:
            patched_read_from_command_line(args=['backup.py'], path=PATH)
        self.assertEqual(e.exception.code, outputs.COMMANDS_INFO)

    # User tries creating a shortcut but misspells 'create' and sees error msg
    def test_receive_invalid_command(self):
        name = 'crete'
        expected_output = outputs.ERROR_MSG['invalid_cmd'](name)

        with self.assertRaises(SystemExit) as e:
            patched_read_from_command_line(
                args=['backup.py', name, 'test', DB['source'],
                      DB['destination'], DB['another_destination']],
                path=PATH)
        self.assertEqual(e.exception.code, expected_output)

    # User creates a shortcut and sees the program's output
    def test_receive_create_command(self):
        expected_output = outputs.create_msg(CREATE_ARGS[2])
        params = patched_read_from_command_line(args=CREATE_ARGS, path=PATH)

        with patch('sys.stdout', new=StringIO()) as mock_output:
            execute_command(command=params[0],
                            params=params[1:],
                            datapath=PATH)
        self.assertEqual(mock_output.getvalue().rstrip(), expected_output)

    # Checks that the shortcut was saved by entering 'show {shortcut}' command
    def test_receive_show_command(self):
        shortcut = CREATE_ARGS[2]
        expected_output = outputs.show_msg(shortcut, DB['source'],
                                           DB['destination'])
        create_1 = patched_read_from_command_line(args=CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_1[0],
                        params=create_1[1:],
                        datapath=PATH)
        show_cmd = patched_read_from_command_line(
            args=['backup.py', 'show', shortcut], path=PATH)

        with patch('sys.stdout', new=StringIO()) as mock_output:
            execute_command(command=show_cmd[0],
                            params=show_cmd[1:],
                            datapath=PATH)
        self.assertEqual(mock_output.getvalue().rstrip(), expected_output)

    # Sees that the destination path is wrong;
    #   Changes the destination path
    @patch('builtins.input', side_effect=['', DB['another_destination']])
    def test_receive_update_command(self, user_input):
        shortcut = CREATE_ARGS[2]
        expected = set(outputs.update_msg(shortcut=shortcut,
            updated_lst=[shortcut]).split('\n'))
        create_cmd = patched_read_from_command_line(args=CREATE_ARGS,
                                                    path=PATH)
        execute_command(command=create_cmd[0],
                        params=create_cmd[1:],
                        datapath=PATH)
        update_cmd = patched_read_from_command_line(
            args=['backup.py', 'update', shortcut], path=PATH)
            
        with patch('sys.stdout', new=StringIO()) as mock_output:
            execute_command(command=update_cmd[0],
                            params=update_cmd[1:],
                            datapath=PATH)
            result = set(mock_output.getvalue().split('\n'))
        self.assertTrue(expected.issubset(result))

        table = sqlite3.connect(PATH).cursor().execute(
            '''SELECT * FROM shortcuts''')
        self.assertEqual(table.fetchone()[2], DB['another_destination'])

    # User creates another shortcut and checks that they are both saved
    #   with 'showall' command
    def test_receive_showall_command(self):
        expected_output = outputs.showall_msg(SHORTCUT_NAMES)
        create_1 = patched_read_from_command_line(args=CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_1[0],
                        params=create_1[1:],
                        datapath=PATH)
        create_2 = patched_read_from_command_line(
            args=ANOTHER_CREATE_ARGS, path=PATH)
        execute_command(command=create_2[0],
                        params=create_2[1:],
                        datapath=PATH)
        showall_cmd = patched_read_from_command_line(
            args=['backup.py', 'showall'], path=PATH)

        with patch('sys.stdout', new=StringIO()) as mock_output:
            execute_command(command=showall_cmd[0],
                            params=showall_cmd[1:],
                            datapath=PATH)
        self.assertEqual(mock_output.getvalue().rstrip(), expected_output)

    # User tries backing up using the saved shortcut but misspells its name
    def test_receive_invalid_shortcut_name(self):
        name = '*_*'
        expected_output = outputs.ERROR_MSG['invalid_cmd'](name)

        with self.assertRaises(SystemExit) as e:
            patched_read_from_command_line(
                args=['backup.py', name], path=PATH)
        self.assertEqual(e.exception.code, expected_output)

    # Enters the correct shortcut's name
    def test_runbackup_command(self):
        create_cmd = patched_read_from_command_line(args=CREATE_ARGS,
                                                    path=PATH)
        execute_command(command=create_cmd[0],
                        params=create_cmd[1:],
                        datapath=PATH)
        command, *params = patched_read_from_command_line(
            args=['backup.py', CREATE_ARGS[2]], path=PATH)

        with self.assertRaises(SystemExit) as e:
            execute_command(command=command, params=params, datapath=PATH)
        self.assertEqual(e.exception.code, outputs.PROGRAM_END)
        shutil.rmtree(DB['destination'])    # TODO clean

    # Decides to delete shortcut from the database
    def test_receive_delete_command(self):
        shortcut = CREATE_ARGS[2]
        expected_output = outputs.delete_msg([shortcut])
        create_1 = patched_read_from_command_line(args=CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_1[0],
                        params=create_1[1:],
                        datapath=PATH)
        create_2 = patched_read_from_command_line(args=ANOTHER_CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_2[0],
                        params=create_2[1:],
                        datapath=PATH)
        delete_cmd = patched_read_from_command_line(
            args=['backup.py', 'delete', shortcut], path=PATH)

        with patch('sys.stdout', new=StringIO()) as mock_output:
            execute_command(command=delete_cmd[0],
                            params=delete_cmd[1:],
                            datapath=PATH)
        self.assertEqual(mock_output.getvalue().rstrip(), expected_output)

        table = sqlite3.connect(PATH).cursor().execute(
            '''SELECT * FROM shortcuts WHERE name = ?''',
            (ANOTHER_CREATE_ARGS[2], ))
        self.assertTrue(table.fetchone())

        table = sqlite3.connect(PATH).cursor().execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (shortcut, ))
        self.assertIsNone(table.fetchone())
