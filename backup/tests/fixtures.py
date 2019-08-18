import pytest
import os
import json

from backup import file_handle


testsource1 = os.path.join(os.getcwd(), 'testsource1')
testdestination1 = os.path.join(os.getcwd(), 'testdestination1')
testsource2 = os.path.join(os.getcwd(), 'testsource2')
testdestination2 = os.path.join(os.getcwd(), 'testdestination2')


DATA = {
    'TEST1': {
        'source': testsource1,
        'destination': [testdestination1]
    },
    'TEST2': {
        'source': testsource2,
        'destination': [testdestination2]
    },
}


@pytest.fixture
def mock_filepath():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    with open(filepath, 'w') as file:
        file.write(json.dumps(DATA))
    yield filepath
    os.remove(filepath)


@pytest.fixture
def mock_data():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    with open(filepath, 'w') as file:
        file.write(json.dumps({}))
    with open(filepath, 'r') as file:
        data = json.load(file)
    yield data
    os.remove(filepath)
