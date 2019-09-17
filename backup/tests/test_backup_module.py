import os
import sys
import sqlite3

from .fixtures import PATH
from backup import backup
import pytest


def test_main_module_creates_shortcut(monkeypatch, PATH):
    expanded_path = os.path.expanduser('~/')
    expected_result = ('abc', expanded_path, expanded_path)
    monkeypatch.setattr(sys, 'argv',
                        ('backup.py', 'create', 'abc', '~/', '~/'))

    backup.main(PATH)
    table = sqlite3.connect(PATH).cursor().execute('SELECT * FROM shortcuts')
    
    assert table.fetchall()[0] == expected_result


def test_main_module_pass_sqlite3_operational_error(monkeypatch):
    expanded_path = os.path.expanduser('~/')
    expected_result = ('abc', expanded_path, expanded_path)
    monkeypatch.setattr(sys, 'argv',
                        ('backup.py', 'create', 'abc', '~/', '~/'))
    path = os.path.join(os.getcwd(), 'testing_pass_error.db')
    with open(path, 'w'):
        pass

    backup.main(path)
    table = sqlite3.connect(path).cursor().execute('SELECT * FROM shortcuts')

    assert table.fetchall()[0] == expected_result
    os.remove(path)
