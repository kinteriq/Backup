import os
import sys
import sqlite3
import unittest
from unittest.mock import patch

from .context import backup  # TODO make unittest work
from backup.commands import read_from_command_line, execute_command
from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION, ANOTHER_DESTINATION

NO_ARGS = ['backup.py']

SHORTCUT_1 = SHORTCUT_NAMES[0]

SHORTCUT_2 = SHORTCUT_NAMES[1]

CREATE_ARGS = ['backup.py', 'create', SHORTCUT_1, SOURCE, DESTINATION]

MISSPELLED_CREATE_COMMAND_ARGS = [
    'backup.py', 'crete', 'test', SOURCE, DESTINATION, ANOTHER_DESTINATION
]

SHOW_ARGS = ['backup.py', 'show', SHORTCUT_1]

UPDATE_ARGS = ['backup.py', 'update', SHORTCUT_1]

ANOTHER_CREATE_ARGS = [
    'backup.py', 'create', SHORTCUT_2, SOURCE, DESTINATION, ANOTHER_DESTINATION
]

SHOWALL_ARGS = ['backup.py', 'showall']

WRONG_SHORTCUT_ARGS = ['backup.py', str(SHORTCUT_1) + '*_*']

BACKUP_ARGS = ['backup.py', SHORTCUT_1]

DELETE_ARGS = ['backup.py', 'delete', SHORTCUT_1]


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

    # User enters empty command
    def test_receive_empty_command(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=NO_ARGS, path=PATH)

    # User tries creating a shortcut but misspells 'create'
    def test_receive_invalid_command(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=MISSPELLED_CREATE_COMMAND_ARGS,
                                           path=PATH)

    # User creates a shortcut and sees the program's output
    @unittest.skip('FINISH')
    def test_receive_create_command(self):
        params = patched_read_from_command_line(args=CREATE_ARGS, path=PATH)
        execute_command(command=params[0], params=params[1:], datapath=PATH)
        assert stdout  # TODO check stdout

    # Checks that the shortcut was saved by entering 'show {shortcut}' command
    @unittest.skip('FINISH')
    def test_receive_show_command(self):
        assert stdout

    # Sees that the destination path is wrong;
    #   Changes the destination path
    user_input = ['', ANOTHER_DESTINATION]

    @patch('builtins.input', side_effect=user_input)
    def test_receive_update_command(self, user_input):
        create_cmd = patched_read_from_command_line(args=CREATE_ARGS,
                                                    path=PATH)
        execute_command(command=create_cmd[0],
                        params=create_cmd[1:],
                        datapath=PATH)
        update_cmd = patched_read_from_command_line(args=UPDATE_ARGS,
                                                    path=PATH)
        execute_command(command=update_cmd[0],
                        params=update_cmd[1:],
                        datapath=PATH)
        table = sqlite3.connect(PATH).cursor().execute(
            '''SELECT * FROM shortcuts''')
        for row in table:
            assert row[2] == ANOTHER_DESTINATION

    # User creates another shortcut and checks that they are both saved
    #   with 'showall' command
    @unittest.skip('FINISH')
    def test_receive_showall_command(self):
        create_1 = patched_read_from_command_line(args=CREATE_ARGS, path=PATH)
        execute_command(command=create_1[0],
                        params=create_1[1:],
                        datapath=PATH)
        create_2 = patched_read_from_command_line(args=ANOTHER_CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_2[0],
                        params=create_2[1:],
                        datapath=PATH)
        showall_cmd = patched_read_from_command_line(args=SHOWALL_ARGS,
                                                     path=PATH)
        execute_command(command=showall_cmd[0],
                        params=showall_cmd[1:],
                        datapath=PATH)
        assert stdout  # TODO check stdout

    # User tries backing up using the saved shortcut but misspells its name
    def test_receive_invalid_shortcut_name(self):
        with self.assertRaises(SystemExit):
            patched_read_from_command_line(args=WRONG_SHORTCUT_ARGS, path=PATH)

    # Enters the correct shortcut's name
    def test_runbackup_command(self):
        create_cmd = patched_read_from_command_line(args=CREATE_ARGS,
                                                    path=PATH)
        execute_command(command=create_cmd[0],
                        params=create_cmd[1:],
                        datapath=PATH)
        command, *params = patched_read_from_command_line(args=BACKUP_ARGS,
                                                          path=PATH)
        with self.assertRaises(SystemExit):
            execute_command(command=command, params=params, datapath=PATH)

    # Decides to delete shortcut from the database
    def test_receive_delete_command(self):
        create_1 = patched_read_from_command_line(args=CREATE_ARGS, path=PATH)
        execute_command(command=create_1[0],
                        params=create_1[1:],
                        datapath=PATH)
        create_2 = patched_read_from_command_line(args=ANOTHER_CREATE_ARGS,
                                                  path=PATH)
        execute_command(command=create_2[0],
                        params=create_2[1:],
                        datapath=PATH)
        delete_cmd = patched_read_from_command_line(args=DELETE_ARGS,
                                                    path=PATH)
        execute_command(command=delete_cmd[0],
                        params=delete_cmd[1:],
                        datapath=PATH)
        table = sqlite3.connect(PATH).cursor().execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (DELETE_ARGS[2], ))
        self.assertIsNone(table.fetchone())


if __name__ == '__main__':
    unittest.main()
