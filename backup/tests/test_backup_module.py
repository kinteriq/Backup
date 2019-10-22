import os
import pytest
import sys
import sqlite3

import backup
from constants import CREATE_1
import outputs


def test_main_module_does_not_raise_exception(monkeypatch, DB_PATH):
    monkeypatch.setattr(sys, 'argv', CREATE_1.args())
    backup.main(DB_PATH)
    table = sqlite3.connect(DB_PATH).cursor().execute('SELECT * FROM shortcuts')
    assert table.fetchall()[0] == CREATE_1.db_content(),\
        'Database content does not equal received args'


def test_wrong_custom_path_to_db(monkeypatch):
    monkeypatch.setattr(sys, 'argv', CREATE_1.args())
    with pytest.raises(SystemExit) as e:
        backup.main('wrong-path/test.db')
    assert e.exconly().endswith(outputs.ERROR_MSG['wrong_custom_datapath']),\
        'Missing wrong custom datapath error message.'


def test_main_module_pass_db_exists_operational_error(monkeypatch, DB_PATH):
    with open(DB_PATH, 'w'):
        pass
    monkeypatch.setattr(sys, 'argv',  CREATE_1.args())
    assert backup.main(DB_PATH) is None,\
        'Did not pass db exists error'
