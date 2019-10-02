import os
import pytest
import sys

from commands import read_from_command_line, execute_command
import outputs
from constants import (DB, SHORTCUT_NAMES, CreateCmd, ShowallCmd,
                       RunbackupCmd)


def test_got_empty_line(monkeypatch, DB_PATH):
    monkeypatch.setattr(sys, 'argv', [])
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=DB_PATH)
    assert outputs.COMMANDS_INFO.rstrip() in e.exconly(),\
        'Documentation is not in the output'


def test_got_invalid_command(monkeypatch, mock_fields_db):
    inst = CreateCmd(cmd='wrongNAME')
    monkeypatch.setattr(sys, 'argv', inst.args())
    with pytest.raises(SystemExit) as e:
        read_from_command_line(datapath=mock_fields_db)
    assert outputs.ERROR_MSG['invalid_cmd'](inst.cmd) in e.exconly(),\
        'Wrong invalid cmd error message'


def test_got_showall_command(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', ShowallCmd().args())
    result = read_from_command_line(datapath=mock_fields_db)
    assert result == ('showall', ),\
        'read_from_command_line() did not return showall args'


def test_got_a_shortcut(monkeypatch, mock_fields_db):
    monkeypatch.setattr(sys, 'argv', RunbackupCmd().args())
    command, *params = read_from_command_line(datapath=mock_fields_db)
    assert (command, params) == (None, [RunbackupCmd().name]),\
        'read_from_command_line() did not return runbackup args'


def test_got_valid_command(monkeypatch, empty_db_cursor, DB_PATH):
    monkeypatch.setattr(sys, 'argv', CreateCmd().args())
    result = read_from_command_line(datapath=DB_PATH)
    assert result == tuple(CreateCmd().args()[1:]),\
        'read_from_command_line() did not return valid create args'


def test_execute_create_command(empty_db_cursor, DB_PATH):
    command, *params = CreateCmd().args()[1:]
    assert execute_command(command=command, params=params,
                           datapath=DB_PATH) is None,\
        'execute_command did not execute correctly'
