import json


def create_json(file: str) -> str:
    with open(file, 'w') as f:
        f.write(json.dumps({}))
    return read_from(file)


def read_from(file: str) -> dict:
    with open(file, 'r') as f:
        file = json.load(f)
    return file


def write_to(file: json, data: dict):
    pass
