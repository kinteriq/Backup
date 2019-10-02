from io import StringIO
import os
import sys
import sqlite3
import shutil
import unittest
from unittest.mock import patch

import outputs
from commands import execute_command
from tests.constants import (PATH, SHORTCUT_NAMES, DB, CreateCmd, 
                             ShowCmd, UpdateCmd, ShowallCmd, RunbackupCmd,
                             DeleteCmd)



CREATED_1 = CreateCmd(name=SHORTCUT_NAMES[0])
CREATED_2 = CreateCmd(name=SHORTCUT_NAMES[1],
                      destination=DB['third_destination'])


def cmd_execution_output_check(args):
    with patch('sys.stdout', new=StringIO()) as mock_output:
        cmd_execution(args)
    return mock_output


def cmd_execution(args):
    with patch.object(sys, 'argv', args):
        execute_command(datapath=PATH)


def get_table_raw(cmd):
    table = sqlite3.connect(PATH).cursor().execute(*cmd)
    return table.fetchone()


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
            cmd_execution(args=['backup.py'])
        self.assertEqual(e.exception.code, outputs.COMMANDS_INFO),\
            'Documentation is not in the output'

    # User tries creating a shortcut but misspells 'create' and sees error msg
    def test_receive_invalid_command(self):
        inst = CreateCmd(cmd='wr0ng')
        expected_output = outputs.ERROR_MSG['invalid_cmd'](inst.cmd)
        with self.assertRaises(SystemExit) as e:
            cmd_execution(args=inst.args())
        self.assertEqual(e.exception.code, expected_output),\
            'Wrong invalid cmd message or no msg at all'

    # User creates a shortcut and sees the program's output
    def test_receive_create_command(self):
        expected_output = outputs.create_msg(CREATED_1.name)
        output = cmd_execution_output_check(CREATED_1.args())
        self.assertEqual(output.getvalue().rstrip(), expected_output),\
            'Create cmd does not execute correctly'

    # Checks that the shortcut was saved by entering 'show {shortcut}' command
    def test_receive_show_command(self):
        expected_output = outputs.show_msg(*CREATED_1.db_content())
        cmd_execution(CREATED_1.args())
        output = cmd_execution_output_check(ShowCmd().args())
        self.assertEqual(output.getvalue().rstrip(), expected_output),\
            'Show cmd does not execute correctly'

    # Sees that the destination path is wrong;
    #   Changes the destination path
    @patch('builtins.input', side_effect=['', DB['third_destination']])
    def test_receive_update_command(self, user_input):
        expected = set(outputs.update_msg(shortcut=CREATED_1.name,
            updated_lst=[CREATED_1.name]).split('\n'))
        cmd_execution(CREATED_1.args())
        output = cmd_execution_output_check(UpdateCmd().args())
        result = set(output.getvalue().split('\n'))
        self.assertTrue(expected.issubset(result)),\
            'Update cmd does not execute correctly'

        self.assertEqual(get_table_raw(('SELECT * FROM shortcuts',))[2],
                                       DB['third_destination']),\
            f'{CREATED_1.name} was not updated in db'

    # User creates another shortcut and checks that they are both saved
    #   with 'showall' command
    def test_receive_showall_command(self):
        expected_output = outputs.showall_msg(SHORTCUT_NAMES)
        cmd_execution(CREATED_1.args())
        cmd_execution(CREATED_2.args())
        output = cmd_execution_output_check(ShowallCmd().args())
        self.assertEqual(output.getvalue().rstrip(), expected_output),\
            'Showall cmd does not execute correctly'

    # Enters the correct shortcut's name
    def test_runbackup_command(self):
        cmd_execution(CREATED_1.args())
        with self.assertRaises(SystemExit) as e:
            cmd_execution(args=RunbackupCmd().args())
        self.assertEqual(e.exception.code, outputs.PROGRAM_END),\
            'Runbackup cmd does not execute correctly'

    # Decides to delete shortcut from the database
    def test_receive_delete_command(self):
        expected_output = outputs.delete_msg([CREATED_1.name])
        cmd_execution(CREATED_1.args())
        cmd_execution(CREATED_2.args())
        output = cmd_execution_output_check(DeleteCmd().args())
        self.assertEqual(output.getvalue().rstrip(), expected_output),\
            'Delete cmd does not execute correctly'
        
        self.assertTrue(get_table_raw(
            ('SELECT * FROM shortcuts WHERE name = ?',
            (CREATED_2.name, )))), f'{CREATED_2.name} should not be deleted'

        self.assertIsNone(get_table_raw(
            ('SELECT * FROM shortcuts WHERE name = ?',
            (CREATED_1.name, )))), f'{CREATED_1.name} should be deleted'