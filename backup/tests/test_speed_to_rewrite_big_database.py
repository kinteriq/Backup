import time

from backup.file_handle import create, write_to_file, read_from
from .fixtures import mock_filepath

BIG_DATA = {i: {i: '', i + i: ''} for i in range(1000)}


def test_time_complexity(mock_filepath):
    begin = time.perf_counter()
    create(mock_filepath)
    write_to_file(data=BIG_DATA, path=mock_filepath)
    read_from(mock_filepath)
    perform_time = time.perf_counter() - begin
    assert perform_time < 0.01
