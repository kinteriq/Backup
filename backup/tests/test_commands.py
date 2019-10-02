import os
import pytest
import sys

from commands import execute_command
import outputs
from unittest.mock import patch
from constants import (DB, VALID_ARGS_WITH_MOCK_DB,
                       CreateCmd, RunbackupCmd)


@pytest.mark.commands
@pytest.mark.parametrize('args', VALID_ARGS_WITH_MOCK_DB)
def test_execute_commands(monkeypatch, mock_fields_db, args):
    monkeypatch.setattr('sys.argv', args)
    try:
        assert execute_command(datapath=mock_fields_db) is None,\
            'execute_command did not execute correctly'
    except OSError: # reading from stdin while output is captured (UpdateCmd)
        with patch('builtins.input', side_effect=['', DB['third_destination']]):
            assert execute_command(datapath=mock_fields_db) is None,\
            'execute_command did not execute correctly'


@pytest.mark.commands
def test_execute_create_cmd(monkeypatch, empty_db_cursor, DB_PATH):
    monkeypatch.setattr('sys.argv', CreateCmd().args())
    assert execute_command(datapath=DB_PATH) is None,\
        'execute_command (create) did not execute correctly'


@pytest.mark.commands
def test_runbackup_cmd(monkeypatch, mock_fields_db):
    monkeypatch.setattr('sys.argv', RunbackupCmd().args())
    with pytest.raises(SystemExit) as e:
        execute_command(datapath=mock_fields_db)
    assert e.exconly().endswith(outputs.PROGRAM_END),\
        'execute_command (runbackup) did not execute correctly'