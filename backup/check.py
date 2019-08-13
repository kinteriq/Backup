# TODO move runner and execute_command out
import sys

import error


def empty(arguments):
    try:
        if not arguments:
            raise error.Empty
    except error.Empty as e:
        sys.exit(e)


def invalid_shortcut_name(data, arguments):
    try:
        not_showall_cmd = arguments[0] != 'showall'
        invalid_name = arguments[0] not in data
        if len(arguments) == 1 and not_showall_cmd and invalid_name:
            raise error.InvalidShortcutName
    except error.InvalidShortcutName as e:
        sys.exit(e)


def invalid_command(commands, arguments):
    try:
        invalid_command = arguments[0] not in commands
        if len(arguments) > 1 and invalid_command:
            raise error.InvalidCommand
    except error.InvalidCommand as e:
        sys.exit(e)


def shortcut_exists(shortcut, data):
    try:
        if shortcut in data:
            raise error.ShortcutExists
    except error.ShortcutExists as e:
        sys.exit(e)
