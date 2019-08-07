import sys

_ERROR_MESSAGE = {
    'wrong_command': 'There is no such command: ',
}

_AVAILABLE_COMMANDS = {
    'create': None,
    'update': None,
    'delete': None,
    'show': None,
    'showall': None,
}


def check_args(args: tuple) -> bool:
    if _shortcut_call(args):
        run_backup(shortcut=args[0])
        return False

    if not _is_valid_command(args):
        raise Exception(_ERROR_MESSAGE['wrong_command'])

    return True


def execute_command() -> str:
    args = sys.argv[1:]
    if check_args(args):
        command, params = args[0], args[1:]
        output = _AVAILABLE_COMMANDS[command](params)
        return output


def run_backup(shortcut: str):
    pass


def _shortcut_call(args: tuple):
    pass


def _is_valid_command(args: tuple):
    if not args:
        return False
