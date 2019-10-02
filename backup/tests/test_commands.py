import os
import pytest
import sys

from commands import execute_command
import outputs
from unittest.mock import patch
from constants import (DB, SHORTCUT_NAMES, VALID_ARGS_WITH_MOCK_DB,
                       CreateCmd, ShowallCmd, RunbackupCmd)


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
