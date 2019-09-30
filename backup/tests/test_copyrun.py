from io import StringIO
import os
import pytest
import shutil
from unittest import mock

import copyrun
from constants import DB


def test_copyall_ok(mock_fields_db):
    """
    Copying all files from backup folder to test folder.
    """
    copyrun.call([DB['name']], mock_fields_db)
    assert set(os.listdir(DB['source'])) == set(os.listdir(DB['destination']))


def _transfer_files():
    shutil.copytree(DB['source'], DB['destination'])
    transferred_files = set()
    for this_dir, _, filenames in os.walk(DB['source']):
        for file in filenames:
            transferred_files.add(os.path.join(this_dir, file))
    return transferred_files


@pytest.mark.xfail(reason='WIP', strict=True)
def test_copy_with_all_replacements(monkeypatch, mock_fields_db):
    transfer = _transfer_files()
    monkeypatch.setattr('sys.stdin', StringIO('all'))
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        copyrun.call([DB['name']], mock_fields_db)
    assert transferred < set(mock_out.getvalue().split())


@pytest.mark.xfail(reason='WIP', strict=True)
def test_copy_without_any_replacements(monkeypatch, mock_fields_db):
    transferred = _transfer_files()
    monkeypatch.setattr('sys.stdin', StringIO('nothing'))
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        copyrun.call([DB['name']], mock_fields_db)
    assert transferred < set(mock_out.getvalue().split())