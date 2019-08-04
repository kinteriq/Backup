import sys

from shortcuts import Shortcuts


_ERROR_MESSAGE = {
    'wrong_command': 'There is no such command: ',
}
_AVAILABLE_COMMANDS = {
    'create': Shortcuts.create,
    'update': None,
    'delete': None,
    'show': None,
    'transfer': None,
    'showall': None,
}
_SHORTCUTS = Shortcuts()


def receive_command():
    args = sys.argv
    cmd = args[1]
    if cmd not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], cmd)
    if cmd == 'showall':
        return cmd
    shortcut = args[2]
    path_from = args[3]
    path_to = set(args[4:])

    return cmd, shortcut, path_from, path_to


def execute_command(command_line):
    command, shortcut, path_from, path_to = command_line
    result = _AVAILABLE_COMMANDS[command](
        _SHORTCUTS,
        shortcut=shortcut,
        path_from=path_from,
        path_to=path_to
    )
    return result


if __name__ == '__main__':
    command_line = receive_command()
    result = execute_command(command_line)
