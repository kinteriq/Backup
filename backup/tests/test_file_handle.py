import os
import pytest

from backup.file_handle import create, read_from, write_to
from .fixtures import mock_data, mock_filepath


def test_create_file():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    create(filepath)
    assert os.path.exists(filepath)
    os.remove(filepath)


def test_read_from(mock_filepath):
    data = read_from(mock_filepath)
    assert data == {}


def test_write_to_file(mock_filepath):
    data = dict(test='writing')
    write_to(mock_filepath, data)
    with open(mock_filepath, 'r') as file:
        assert file.read() == '{"test": "writing"}'
