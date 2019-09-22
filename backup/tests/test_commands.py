import os
import pytest
import sqlite3
import sys

from .context import backup
from backup.commands import read_from_command_line, execute_command
from backup.check import MSG as error_message
from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION, mock_fields_db

EMPTY_ARGS = []

INVALID_CMD_ARGS = ['backup.py', 'messed', 'up']

HELP_ARGS = ['backup.py', 'help']

SHOWALL_ARGS = ['backup.py', 'showall']

BACKUP_ARGS = ['backup.py'] + list(SHORTCUT_NAMES)

VALID_CMD_ARGS = ['backup.py', 'create', 'NAME', SOURCE, DESTINATION]


def test_help_command(monkeypatch):
    monkeypatch.setattr(sys, 'argv', HELP_ARGS)
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=PATH)
    assert backup.commands.__doc__.strip() in e.exconly()


def test_got_empty_line(monkeypatch, PATH):
    monkeypatch.setattr(sys, 'argv', EMPTY_ARGS)
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=PATH)
    assert error_message['empty'] in e.exconly()


def test_got_invalid_command(monkeypatch, mock_fields_db, PATH):
    monkeypatch.setattr(sys, 'argv', INVALID_CMD_ARGS)
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=PATH)
    assert error_message['invalid_cmd'] in e.exconly()


def test_got_showall_command(monkeypatch, mock_fields_db, PATH):
    monkeypatch.setattr(sys, 'argv', SHOWALL_ARGS)
    assert read_from_command_line(datapath=PATH) == ('showall', )


def test_got_a_shortcut(monkeypatch, mock_fields_db, PATH):
    monkeypatch.setattr(sys, 'argv', BACKUP_ARGS)
    command, *params = read_from_command_line(datapath=PATH)
    assert (command, params) == (None, BACKUP_ARGS[1:])


def test_got_valid_command(monkeypatch, mock_fields_db, PATH):
    monkeypatch.setattr(sys, 'argv', VALID_CMD_ARGS)
    result = read_from_command_line(datapath=PATH)
    assert result == ('create', 'NAME', SOURCE, DESTINATION)


def test_execute_create_command(mock_fields_db, PATH):
    command, *params = VALID_CMD_ARGS[1:]
    assert execute_command(command=command, params=params,
                           datapath=PATH) is None
