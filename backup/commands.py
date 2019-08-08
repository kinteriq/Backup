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

import error

_COMMANDS = {
    'create': None,
    'update': None,
    'delete': None,
    'show': None,
    'showall': None,
}


def check_args(args) -> bool:
    if _empty(args):
        print(error.NoArgs())
        sys.exit()

    if _shortcut_name(args):
        run_backup(shortcut=args[0])
        return False

    if not _valid_command(args):
        print(error.InvalidCommand())
        sys.exit()

    return True


def execute_command() -> str:
    args = sys.argv[1:]
    if check_args(args):
        command, params = args[0], args[1:]
        output = _COMMANDS[command](params)
        return output


def run_backup(shortcut):
    pass


def _empty(args) -> bool:
    if not args:
        return True
    return False


def _shortcut_name(args) -> bool:
    if len(args) == 1 and args[0] in ['NAME']:
        return True
    return False


def _valid_command(args) -> bool:
    if args[0] in _COMMANDS:
        return True
    return False
