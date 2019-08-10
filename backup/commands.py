#     Backup is a tool which makes day-to-day backups easier.
#
#     Copyright (C) 2019  kinteriq
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys

from shortcuts import Shortcuts as Shortcuts
import error

COMMANDS = {
    'create': Shortcuts.create,
    'update': Shortcuts.update,
    'delete': Shortcuts.delete,
    'show': Shortcuts.show,
    'showall': Shortcuts.showall,
}


def read_from_command_line(data: dict) -> list:
    args = sys.argv[1:]  # exclude 'backup.py'
    try:
        _is_empty(args)
        _is_showall(data=data, args=args)
        _is_shortcut_name(data=data, args=args)
        _is_invalid_command(args)
    except error.Empty as e:
        sys.exit(e)
    except error.InvalidCommand as e:
        sys.exit(e)
    return args


def execute_command(data: dict, command, params) -> str:
    output = COMMANDS[command](data=data, arguments=params)
    return output


def _is_empty(args):
    if not args:
        raise error.Empty


def _is_shortcut_name(data, args):
    valid_name = args[0] in data
    if len(args) == 1 and valid_name:
        _run_backup(shortcut=args[0])
        sys.exit('BACKUP IS FINISHED')


def _run_backup(shortcut):
    pass


def _is_invalid_command(args):
    if args[0] not in COMMANDS:
        raise error.InvalidCommand


def _is_showall(data, args):
    if args[0] == 'showall':
        all_shortcuts = COMMANDS['showall'](data)
        sys.exit(all_shortcuts)
