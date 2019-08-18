import os

from .fixtures import mock_filepath, DATA
from backup import runner


def setup():
    for shortcut in DATA:
        os.mkdir(DATA[shortcut]['source'])


def teardown():
    for shortcut in DATA:
        os.removedirs(DATA[shortcut]['source'])
        for destination in DATA[shortcut]['destination']:
            os.removedirs(destination)


def test_copy_all_ok(mock_filepath):
    """
    Tests that the function return True if copying was successful.
    """
    shortcuts = list(DATA.keys())
    assert runner.copy_all(shortcuts=shortcuts, path=mock_filepath)
