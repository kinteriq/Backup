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

from shortcuts import Shortcuts as shortcuts
import error

_COMMANDS = {
    'create': shortcuts.create,
    'update': None,
    'delete': None,
    'show': None,
    'showall': None,
}
temp = shortcuts({})


def execute_command() -> str:
    args = sys.argv[1:]         # exclude 'backup.py'
    _is_command(args)
    command, params = args[0], args[1:]
    output = _COMMANDS[command](temp, arguments=params)
    return output


def _is_command(args):
    for check in [_empty, _shortcut_name, _invalid_command]:
        try:
            check(args)
        except error.NoArgs as e:
            sys.exit(e)
        except error.InvalidCommand as e:
            sys.exit(e)
        except SystemExit:
            sys.exit('FINISH')
    return True


def _empty(args):
    if not args:
        raise error.NoArgs


def _shortcut_name(args):
    valid_name = args[0] in ['NAME']
    if len(args) == 1 and valid_name:
        run_backup(shortcut=args[0])
        sys.exit()


def run_backup(shortcut):
    pass


def _invalid_command(args):
    if args[0] not in _COMMANDS:
        raise error.InvalidCommand
