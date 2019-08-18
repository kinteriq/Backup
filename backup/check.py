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

MSG = {
    'invalid_cmd': 'There is no such command (try "help"): ',
    'empty': 'Zero arguments provided.',
    'invalid_shortcut': 'There is no such shortcut saved: ',
    'created_shortcut_exists':
    'Shortcut is already in the database. Try "update" command.',
    'empty_data':
    'There is no shortcuts saved. Try "create" or "help" command.',
}


def created_shortcut_exists(shortcut, data):
    if shortcut in data:
        sys.exit(MSG['created_shortcut_exists'])


def valid_shortcut(shortcut, data):
    if shortcut in data:
        return True
    sys.exit(MSG['invalid_shortcut'] + shortcut)


def valid_command(all_commands, command):
    if command in all_commands:
        return True
    sys.exit(MSG['invalid_cmd'] + command)


def data_not_empty(data):
    if data:
        return True
    sys.exit(MSG['empty_data'])


ARGS_VALIDATION = {
    'create':
    lambda args, data: all(
        [len(args) >= 4,
         created_shortcut_exists(shortcut=args[1], data=data)]),
    'update':
    lambda args, data: all(
        [len(args) == 2,
         valid_shortcut(shortcut=args[1], data=data)]),
    'delete':
    lambda args, data: all(
        [len(args) == 2,
         valid_shortcut(shortcut=args[1], data=data)]),
    'show':
    lambda args, data: all([len(args) >= 2] + [
        valid_shortcut(shortcut=arg, data=data) for arg in args[1:]
    ]),
    'showall':
    lambda args, data: all(
        [len(args) == 1,
         data_not_empty(data), args[0] == 'showall']),
}


class CommandLine:
    def __init__(self, data, arguments, all_commands):
        self.data = data
        self.arguments = arguments
        self.commands = all_commands

    def complete(self):
        """
        Performs all checks in the class.
        """
        self.empty()
        valid_args = None
        try:
            valid_args = self.runbackup_cmd()
        except SystemExit:
            valid_args = self.valid_cmd()
        return valid_args

    def empty(self):
        if not self.arguments:
            sys.exit(MSG['empty'])

    def valid_cmd(self):
        """
        Check if command is valid;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        command = self.arguments[0]
        valid_command(all_commands=self.commands, command=command)
        ARGS_VALIDATION[command](self.arguments, self.data)
        return tuple(self.arguments)

    def runbackup_cmd(self):
        """
        Check if every argument is a saved shortcut;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        for arg in self.arguments:
            valid_shortcut(shortcut=arg, data=self.data)
        return (None, ) + tuple(self.arguments)
