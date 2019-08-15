import sys

import error


def empty(arguments):
    try:
        if not arguments:
            raise error.Empty
    except error.Empty as e:
        sys.exit(e)


def invalid_shortcut_name(data, arguments, commands):
    try:
        not_showall_cmd = arguments[0] != 'showall'
        invalid_name = arguments[0] not in data
        not_command = arguments[0] not in commands
        if (len(arguments) == 1 and not_showall_cmd and invalid_name
                and not_command):
            raise error.InvalidShortcutName
    except error.InvalidShortcutName as e:
        sys.exit(e)


def invalid_command(commands, arguments):
    """
    :param: commands:
        iterable; has all available commands
    """
    try:
        invalid_command = arguments[0] not in commands
        if len(arguments) > 1 and invalid_command:
            raise error.InvalidCommand
        _command_with_zero_arguments(commands=commands, arguments=arguments)
    except error.InvalidCommand as e:
        sys.exit(e)


def shortcut_exists(shortcut, data):
    try:
        if shortcut in data:
            raise error.ShortcutExists
    except error.ShortcutExists as e:
        sys.exit(e)


def _command_with_zero_arguments(commands, arguments):
    """
    Checks if command is correct but has no arguments.

    :param: commands:
        iterable; has all available commands
    """
    try:
        command = arguments[0]
        valid_cmd = command in commands
        not_showall = command != 'showall'
        if len(arguments) == 1 and valid_cmd and not_showall:
            raise error.CommandWithZeroArgs
    except error.CommandWithZeroArgs as e:
        sys.exit(e)
