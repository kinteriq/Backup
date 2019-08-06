import sys

from file_handler import get_data
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


def receive_command(data=get_data) -> tuple:
    if sys.argv[1] in data:
        shortcut = sys.argv[1]
        return shortcut, None, data

    command = sys.argv[1]
    if command not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], command)
        sys.exit()
    arguments = sys.argv[2:]

    return command, arguments, data


def execute_command(command_line: tuple) -> str:
    command, arguments, data = command_line
    if arguments:
        output_result = _AVAILABLE_COMMANDS[command](Shortcuts(data),
                                                     arguments)
        return output_result
    shortcut = command
    return f'Successfully backed up: {shortcut}.'
