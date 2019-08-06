import sys

from file_handler import create_json, read_from
from shortcuts import Shortcuts

_ERROR_MESSAGE = {
    'wrong_command': 'There is no such command: ',
}
_AVAILABLE_COMMANDS = {
    'create': Shortcuts.create,
    'update': Shortcuts.update,
    'delete': None,
    'show': Shortcuts.show,
    'showall': None,
}

try:
    DATA = read_from('shortcuts.json')
except FileNotFoundError as exc:
    DATA = create_json('shortcuts.json')


def receive_command() -> tuple:
    if sys.argv[1] in DATA:
        shortcut = sys.argv[1]
        return shortcut,

    command = sys.argv[1]
    if command not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], command)
        sys.exit()
    arguments = sys.argv[2:]

    return command, arguments


def execute_command(command_line: tuple) -> str:
    command, arguments = command_line
    output_result = _AVAILABLE_COMMANDS[command](Shortcuts(DATA), arguments)
    return output_result


if __name__ == '__main__':
    received_line = receive_command()
    output = execute_command(received_line)
