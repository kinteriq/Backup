import os
import pytest
import sys

from commands import read_from_command_line, execute_command
import outputs
from constants import DB, SHORTCUT_NAMES


def test_got_empty_line(monkeypatch, DB_PATH):
    monkeypatch.setattr(sys, 'argv', [])
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=DB_PATH)
    assert outputs.COMMANDS_INFO.rstrip() in e.exconly()


def test_got_invalid_command(monkeypatch, mock_fields_db):
    name = 'wrongNAME'
    monkeypatch.setattr(sys, 'argv', ['backup.py', name])
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=mock_fields_db)
    assert outputs.ERROR_MSG['invalid_cmd'](name) in e.exconly()


def test_got_showall_command(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', ['backup.py', 'showall'])
    assert read_from_command_line(datapath=mock_fields_db) == ('showall', )


def test_got_a_shortcut(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', ['backup.py'] + list(SHORTCUT_NAMES))
    command, *params = read_from_command_line(datapath=mock_fields_db)
    assert (command, params) == (None, SHORTCUT_NAMES)


def test_got_valid_command(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv',
        ['backup.py', 'create', 'NAME', DB['source'], DB['destination']])
    result = read_from_command_line(datapath=mock_fields_db)
    assert result == ('create', 'NAME', DB['source'], DB['destination'])


def test_execute_create_command(mock_fields_db):
    command, *params = ['create', 'NAME', DB['source'], DB['destination']]
    assert execute_command(command=command, params=params,
                           datapath=mock_fields_db) is None
