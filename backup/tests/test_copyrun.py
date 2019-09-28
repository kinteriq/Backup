from io import StringIO
import os
import pytest
import sqlite3
import shutil
from unittest import mock

from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION, mock_fields_db
from backup import copyrun


def test_copyall_ok(mock_fields_db):
    """
    Copying all files from backup folder to test folder.
    """
    copyrun.call([SHORTCUT_NAMES[0]], mock_fields_db)
    assert set(os.listdir(SOURCE)) == set(os.listdir(DESTINATION))
    shutil.rmtree(DESTINATION)
    

@pytest.mark.xfail(reason='WIP', strict=True)
def test_copy_with_all_replacements(monkeypatch, mock_fields_db):
    shutil.copytree(SOURCE, DESTINATION)
    transferred_files = set()
    for this_dir, _, filenames in os.walk(SOURCE):
        for file in filenames:
            transferred_files.add(os.path.join(this_dir, file))
    monkeypatch.setattr('sys.stdin', StringIO('all'))
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        copyrun.call([SHORTCUT_NAMES[0]], mock_fields_db)
    assert transferred_files < set(mock_out.getvalue().split())
    shutil.rmtree(DESTINATION)


@pytest.mark.xfail(reason='WIP', strict=True)
def test_copy_without_any_replacements(monkeypatch, mock_fields_db):
    shutil.copytree(SOURCE, DESTINATION)
    transferred_files = set()
    for this_dir, _, filenames in os.walk(SOURCE):
        for file in filenames:
            transferred_files.add(os.path.join(this_dir, file))
    monkeypatch.setattr('sys.stdin', StringIO('nothing'))
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        copyrun.call([SHORTCUT_NAMES[0]], mock_fields_db)
    assert transferred_files < set(mock_out.getvalue().split())
    shutil.rmtree(DESTINATION)
