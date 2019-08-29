import os
import pytest
import sqlite3
import sys

from .context import backup
from backup.commands import read_from_command_line, execute_command
from backup.check import MSG as error_message
from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION

EMPTY_ARGS = []

INVALID_CMD_ARGS = ['backup.py', 'messed', 'up']

SHOWALL_ARGS = ['backup.py', 'showall']

BACKUP_ARGS = ['backup.py'] + list(SHORTCUT_NAMES)

VALID_CMD_ARGS = ['backup.py', 'create', 'NAME', SOURCE, DESTINATION]


class TestReadFromCommandLine():
    def setup_method(self):
        connection = sqlite3.connect(PATH)
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE shortcuts
            (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
        first_name = (SHORTCUT_NAMES[0], 'from/path_1', 'to/path_1')
        cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', first_name)
        second_name = (SHORTCUT_NAMES[1], 'from/path_2', 'to/path_2')
        cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', second_name)
        connection.commit()
        connection.close()

    def teardown_method(self):
        os.remove(PATH)

    def test_got_empty_line(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', EMPTY_ARGS)
        with pytest.raises(SystemExit) as e:
            read_from_command_line(datapath=PATH)
        assert error_message['empty'] in e.exconly()

    def test_got_invalid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', INVALID_CMD_ARGS)
        with pytest.raises(SystemExit) as e:
            read_from_command_line(datapath=PATH)
        assert error_message['invalid_cmd'] in e.exconly()

    def test_got_showall_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', SHOWALL_ARGS)
        assert read_from_command_line(datapath=PATH) == ('showall', )

    def test_got_a_shortcut(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', BACKUP_ARGS)
        command, *params = read_from_command_line(datapath=PATH)
        assert (command, params) == (None, BACKUP_ARGS[1:])

    def test_got_valid_command(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', VALID_CMD_ARGS)
        result = read_from_command_line(datapath=PATH)
        assert result == ('create', 'NAME', SOURCE, DESTINATION)

    def test_execute_create_command(self):
        command, *params = VALID_CMD_ARGS[1:]
        assert execute_command(command=command, params=params,
                               datapath=PATH) is None
