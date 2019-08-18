import os
import pytest
import json

from backup.file_handle import (retreive, create, read_from, write_to_file,
                                get_shortcut_paths)
from .fixtures import mock_filepath, DATA


def test_retreive_existed_file(mock_filepath):
    assert retreive(file=mock_filepath) == DATA


def test_retreive_non_existent_file():
    path = os.path.join(os.getcwd(), 'does_not_exist')
    assert retreive(file=path) == {}
    os.remove(path)


def test_create_file():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    create(file=filepath)
    assert os.path.exists(filepath)
    os.remove(filepath)


def test_read_from(mock_filepath):
    data = read_from(file=mock_filepath)
    assert data == DATA


def test_write_to_file(mock_filepath):
    data = dict(test='writing')
    write_to_file(data=data, path=mock_filepath)
    with open(mock_filepath, 'r') as file:
        assert file.read() == '{"test": "writing"}'


def test_get_shortcut_paths(mock_filepath):
    with open(mock_filepath, 'w') as file:
        file.write(json.dumps({'TEST': 'some_info'}))
    expected_output = 'some_info'
    output = get_shortcut_paths(shortcut='TEST', datapath=mock_filepath)
    assert output == expected_output
