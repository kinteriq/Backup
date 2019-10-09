from io import StringIO
import os
import pytest
import shutil
from unittest import mock

import copyrun
from constants import CREATE_1


def test_copyall_ok(mock_fields_db):
    """
    Copying all files from backup folder to test folder.
    """
    copyrun.call([CREATE_1.name], mock_fields_db)

    assert set(os.listdir(CREATE_1.source)) == set(os.listdir(CREATE_1.destinations[0])),\
        'Did not copied correctly to the first destination'

    assert set(os.listdir(CREATE_1.source)) == set(os.listdir(CREATE_1.destinations[1])),\
        'Did not copied correctly to the second destination'


def test_copy_with_all_replacements(monkeypatch, mock_fields_db):
    transfer = _transfer_files()
    monkeypatch.setattr('sys.stdin', StringIO('all'))
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        copyrun.call([CREATE_1.name], mock_fields_db)
    assert transfer < set(mock_out.getvalue().split())


@pytest.mark.xfail(strict=True)
def test_copy_without_any_replacements(monkeypatch, mock_fields_db):
    with mock.patch('sys.stdout', new=StringIO()) as mock_out:
        monkeypatch.setattr('sys.stdin', StringIO('nothing'))
        copyrun.call([CREATE_1.name], mock_fields_db)
    assert len(mock_out.getvalue().split()) == 10


def _transfer_files():
    shutil.copytree(CREATE_1.source, CREATE_1.destinations[0])
    transferred_files = set()
    for this_dir, _, filenames in os.walk(CREATE_1.source):
        for file in filenames:
            if this_dir != CREATE_1.source:
                filepath = os.path.join(CREATE_1.destinations[0],
                                        os.path.split(this_dir)[1],
                                        file)
            else:
                filepath = os.path.join(CREATE_1.destinations[0], file)
            transferred_files.add(filepath)
    return transferred_files