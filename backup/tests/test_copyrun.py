import os
import pytest
import sqlite3
import shutil

from .fixtures import PATH, SHORTCUT_NAMES, SOURCE, DESTINATION, mock_fields_db
from backup import copyrun


def test_copyall_ok(mock_fields_db, PATH):
    """
    Copying all files from backup folder to test folder.
    """
    copyrun.call([SHORTCUT_NAMES[0]], PATH)
    assert set(os.listdir(SOURCE)) == set(os.listdir(DESTINATION))
    shutil.rmtree(DESTINATION)


@pytest.mark.skip('FINISH')
def test_copy_with_replacements():
    finish


@pytest.mark.skip('FINISH')
def test_copy_without_any_replacements():
    finish
