import sys

import backup.backup
from .fixtures import mock_data


VALID_CMD_ARGS = ['backup.py', 'create', 'TEST', 'from/path', 'to/path']


def test_backup_module_with_valid_command(monkeypatch, mock_data):
    monkeypatch.setattr(sys, 'argv', VALID_CMD_ARGS)
    assert backup.backup.main(data=mock_data)
