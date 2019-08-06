import sys

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
SHORTCUTS = Shortcuts()


def receive_command() -> tuple:
    command = sys.argv[1]
    if command not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], command)
        sys.exit()
    arguments = sys.argv[2:]

    return command, arguments


def execute_command(command_line: tuple) -> str:
    command, arguments = command_line
    output_result = _AVAILABLE_COMMANDS[command](
        SHORTCUTS,
        arguments
    )
    return output_result


if __name__ == '__main__':
    received_line = receive_command()
    output = execute_command(received_line)
