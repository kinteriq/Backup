import pytest
import os
import json


@pytest.fixture
def mock_filepath():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    with open(filepath, 'w') as file:
        file.write(json.dumps({}))
    yield filepath
    os.remove(filepath)


@pytest.fixture
def mock_data():
    filepath = os.path.join(os.getcwd(), 'test_shortcuts.json')
    with open(filepath, 'w') as file:
        file.write(json.dumps({}))
    with open(filepath, 'r') as  file:
        data = json.load(file)
    yield data
    os.remove(filepath)
