import pytest
import os
import sqlite3

# TODO create fixture with mock dirpaths

PATH = os.path.join(os.getcwd(), 'test.db')
SHORTCUT_NAMES = ('TEST_1', 'TEST_2')

SOURCE = os.path.join(os.getcwd(), 'backup')
DESTINATION = os.path.join(os.getcwd(), 'testBackup')
ANOTHER_DESTINATION = os.path.join(os.getcwd(), 'testBackup_2')
