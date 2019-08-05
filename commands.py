import sys

from shortcuts import Shortcuts


_ERROR_MESSAGE = {
    'wrong_command': 'There is no such command: ',
}
_AVAILABLE_COMMANDS = {
    'create': Shortcuts.create,
    'update': None,
    'delete': None,
    'show': Shortcuts.show,
    'showall': None,
}
_SHORTCUTS = Shortcuts()


def receive_command() -> tuple:
    command = sys.argv[1]
    if command not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], command)
        return
    arguments = sys.argv[2:]

    return command, arguments


def execute_command(command_line: tuple) -> str:
    command, arguments = command_line
    result = _AVAILABLE_COMMANDS[command](
        _SHORTCUTS,
        arguments
    )
    return result


if __name__ == '__main__':
    command_line = receive_command()
    result = execute_command(command_line)
