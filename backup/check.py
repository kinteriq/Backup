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
import os
import sqlite3

from database import db_connect

MSG = {
    'invalid_cmd': 'No such command (try "help"): ',
    'empty': 'Zero arguments provided.',
    'invalid_shortcut': 'No such shortcut saved: ',
    'created_shortcut_exists':
    'Shortcut is already in the database. Try "update" command.',
    'no_data': 'No shortcuts saved. Try "create" or "help" command.',
    'wrong_path': 'Directory does not exist:\n\t'
}


class CommandLine:
    """
    Check all arguments in command line are correct.
    """
    def __init__(self, datapath, arguments, all_commands):
        self.data = datapath
        self.arguments = arguments
        self.commands = all_commands

    def complete(self):
        """
        Performs all checks in the class.
        """
        valid_args = None
        self.empty()
        try:
            # see if arg[-s] is a [are] shortcut[-s]
            valid_args = self.backup_args()
        except SystemExit:
            # see if arg[-s] is [are] a correct command
            valid_args = self.command_args()
        return valid_args

    def empty(self):
        if not self.arguments:
            raise SystemExit(MSG['empty'])

    def backup_args(self):
        """
        Check if every argument is a saved shortcut;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        for arg in self.arguments:
            Validate.shortcut(args=arg, datapath=self.data)
        return (None, ) + tuple(self.arguments)

    def command_args(self):
        """
        Check if the command is valid;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        command = self.arguments[0]
        Validate.command(available_cmds=self.commands, command=command)
        if Validate.cmd_args[command](args=self.arguments, data=self.data):
            return tuple(self.arguments)


class Validate:
    cmd_args = {
        'create':
        lambda args, data: all([
            len(args) >= 4,
            not Validate.created_shortcut_exists(args=args[1], datapath=data)
        ]),
        'update':
        lambda args, data: all(
            [len(args) == 2,
             Validate.shortcut(args=args[1], datapath=data)]),
        'delete':
        lambda args, data: any([
            len(args) >= 2,
            Validate.shortcut(args=args[1], datapath=data)
            if len(args) == 2 else False
        ]),
        'show':
        lambda args, data: any([
            len(args) >= 2,
            Validate.shortcut(args=args[1], datapath=data)
            if len(args) == 2 else False
        ]),
        'showall':
        lambda args, data: all([
            len(args) == 1,
            Validate.data_not_empty(datapath=data), args[0] == 'showall'
        ]),
    }

    def command(command, available_cmds):
        if command in available_cmds:
            return True
        raise SystemExit(MSG['invalid_cmd'] + command)

    @db_connect
    def created_shortcut_exists(shortcut, datapath, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if exists:
            raise SystemExit(MSG['created_shortcut_exists'])
        return False

    @db_connect
    def shortcut(shortcut, datapath, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if not exists:
            raise SystemExit(MSG['invalid_shortcut'] + shortcut)
        return True

    @db_connect
    def data_not_empty(args, datapath, db_cursor):
        try:
            selection = db_cursor.execute(
                '''SELECT EXISTS (SELECT * FROM shortcuts)''')
            exists = selection.fetchone()[0]
            if not exists:
                raise SystemExit(MSG['no_data'])
            return True

        except sqlite3.OperationalError:
            raise SystemExit(MSG['no_data'])


def dir_path(path):
    if not os.path.exists(path):
        raise SystemExit(MSG['wrong_path'] + path)
    if path.startswith('~'):
        return os.path.join(os.path.expanduser('~'), path[2:])
    return path
