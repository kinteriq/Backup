import os
import sys
import sqlite3

import backup
from constants import CREATE_1


def test_main_module_does_not_raise_exception(monkeypatch, DB_PATH):
    monkeypatch.setattr(sys, 'argv', CREATE_1.args())
    backup.main(DB_PATH)
    table = sqlite3.connect(DB_PATH).cursor().execute('SELECT * FROM shortcuts')
    assert table.fetchall()[0] == CREATE_1.db_content(),\
        'Database content does not equal received args'


def test_main_module_pass_db_exists_operational_error(monkeypatch, DB_PATH):
    with open(DB_PATH, 'w'):
        pass
    monkeypatch.setattr(sys, 'argv',  CREATE_1.args())
    assert backup.main(DB_PATH) is None, 'Did not pass db exists error'
