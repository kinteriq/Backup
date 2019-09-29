import os
import pytest
import sqlite3
import sys

from .context import backup
from backup.commands import read_from_command_line, execute_command
from backup import outputs
from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION, mock_fields_db

EMPTY_ARGS = []

INVALID_CMD_ARGS = ['backup.py', 'messed', 'up']

SHOWALL_ARGS = ['backup.py', 'showall']

BACKUP_ARGS = ['backup.py'] + list(SHORTCUT_NAMES)

VALID_CMD_ARGS = ['backup.py', 'create', 'NAME', SOURCE, DESTINATION]


def test_got_empty_line(monkeypatch, PATH):
    monkeypatch.setattr(sys, 'argv', EMPTY_ARGS)
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=PATH)
        assert outputs.COMMANDS_INFO.rstrip() in e.exconly()


def test_got_invalid_command(monkeypatch, mock_fields_db):
    name = INVALID_CMD_ARGS[1]
    monkeypatch.setattr(sys, 'argv', INVALID_CMD_ARGS)
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=mock_fields_db)
        assert outputs.ERROR_MSG['invalid_cmd'](name) in e.exconly()


def test_got_showall_command(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', SHOWALL_ARGS)
    assert read_from_command_line(datapath=mock_fields_db) == ('showall', )


def test_got_a_shortcut(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', BACKUP_ARGS)
    command, *params = read_from_command_line(datapath=mock_fields_db)
    assert (command, params) == (None, BACKUP_ARGS[1:])


def test_got_valid_command(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', VALID_CMD_ARGS)
    result = read_from_command_line(datapath=mock_fields_db)
    assert result == ('create', 'NAME', SOURCE, DESTINATION)


def test_execute_create_command(mock_fields_db):
    command, *params = VALID_CMD_ARGS[1:]
    assert execute_command(command=command, params=params,
                           datapath=mock_fields_db) is None
