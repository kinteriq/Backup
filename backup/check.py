# TODO move runner and execute_command out
import sys

from commands import execute_command
import error
import runner
from file_handle import DATABASE


def empty(arguments):
    if not arguments:
        raise error.Empty


def shortcut_name(data, arguments):
    valid_name = arguments[0] in data
    if len(arguments) == 1 and valid_name:
        message = runner.copy_all(shortcut=arguments[0])
        sys.exit(message)


def invalid_command(commands, arguments):
    valid_command = arguments[0] in commands
    if len(arguments) > 1 and not valid_command:
        raise error.InvalidCommand


def showall(arguments):
    if arguments[0] == 'showall':
        all_shortcuts = execute_command(command='showall',
                                        params=None,
                                        data=DATABASE)
        sys.exit(all_shortcuts)
