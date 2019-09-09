import os
import pytest
import sqlite3

from .fixtures import PATH, SOURCE, DESTINATION, mock_fields_db
from backup import copyrun

DATA_1 = ('testing', SOURCE, DESTINATION)


def test_copyall_ok(mock_fields_db, PATH):
    assert copyrun.call(['testing'], PATH) is True


@pytest.mark.skip('FINISH')
def test_copy_with_replacements():
    finish


@pytest.mark.skip('FINISH')
def test_copy_without_any_replacements():
    finish
