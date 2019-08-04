import sys


_ERROR_MESSAGE = {
    'wrong_command': 'There is no such command: ',
}
_AVAILABLE_COMMANDS = (
    'create',
    'update',
    'delete',
    'show',
    'transfer',
    'showall'
)


def receive_command():
    args = sys.argv
    cmd = args[1]
    if cmd not in _AVAILABLE_COMMANDS:
        print(_ERROR_MESSAGE['wrong_command'], cmd)
    if cmd == 'showall':
        return cmd
    shortcut_name = args[2]
    path_from = args[3]
    path_to = set(args[4:])

    return cmd, shortcut_name, path_from, path_to


if __name__ == '__main__':
    received = receive_command()
