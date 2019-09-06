from io import StringIO
import os
import pytest
import sqlite3
from unittest import mock

from backup import shortcuts
from .fixtures import PATH, SOURCE, DESTINATION, ANOTHER_DESTINATION

NAME = 'NAME-1'

ANOTHER_NAME = 'NAME-2'

CREATE_ARGS = [NAME, SOURCE, DESTINATION, ANOTHER_DESTINATION]

ANOTHER_CREATE_ARGS = [ANOTHER_NAME, SOURCE, DESTINATION]

DELETE_ARGS = [NAME, 'wrong_NAME']

SHOW_ARGS = [NAME, 'wrong_NAME']

SHOWALL_ARGS = [NAME, ANOTHER_NAME]

WRONG_PATH_ARGS = [NAME, 'wrong_path', 'path']


def setup_module():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    connection.commit()
    connection.close()


def teardown_module():
    os.remove(PATH)


def test_wrong_path_name():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    with pytest.raises(SystemExit) as e:
        shortcuts.create(args=WRONG_PATH_ARGS, datapath=PATH)
    assert 'Directory does not exist' in e.exconly()


def test_shortcut_is_created():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')
    expected_result = tuple(CREATE_ARGS[:2] + [', '.join(CREATE_ARGS[2:])])
    for row in selection:
        assert expected_result == row


def test_update_shortcut(monkeypatch):
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    # shortcuts.create(args=CREATE_ARGS, datapath=PATH)     # TODO make independent
    with mock.patch('builtins.input', side_effect=['', ANOTHER_DESTINATION]):
        shortcuts.update(args=[CREATE_ARGS[0]], datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')
    expected_result = tuple(CREATE_ARGS[:2] + [ANOTHER_DESTINATION])
    for row in selection:
        assert expected_result == row


def test_delete_shortcut():
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    shortcuts.delete(args=DELETE_ARGS, datapath=PATH)
    selection = cursor.execute('''SELECT * FROM shortcuts''')  # TODO adjust
    for row in selection:
        assert not row


@pytest.mark.skip('FINISH')
def test_delete_many_shortcuts():
    assert fail


def test_show_shortcut():
    destinations = ', '.join([DESTINATION, ANOTHER_DESTINATION])
    expected_output = (f'NAME:\n\t{NAME}\n'
                       f'SOURCE:\n\t{SOURCE}\n'
                       f'DESTINATIONS:\n\t{destinations}\n\n')
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    shortcuts.create(args=CREATE_ARGS, datapath=PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.show(args=SHOW_ARGS, datapath=PATH)
        assert mock_output.getvalue() == expected_output


def test_showall():
    expected_output = f'SAVED NAMES:\n\t{NAME}\n\t{ANOTHER_NAME}\n\n'
    connection = sqlite3.connect(PATH)
    cursor = connection.cursor()
    # shortcuts.create(args=CREATE_ARGS, datapath=PATH) # TODO independent
    shortcuts.create(args=ANOTHER_CREATE_ARGS, datapath=PATH)
    with mock.patch('sys.stdout', new=StringIO()) as mock_output:
        shortcuts.showall(args=SHOWALL_ARGS, datapath=PATH)
        assert mock_output.getvalue() == expected_output
