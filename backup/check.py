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

import sqlite3
import sys

from shortcuts import db_connect


MSG = {
    'invalid_cmd': 'There is no such command (try "help"): ',
    'empty': 'Zero arguments provided.',
    'invalid_shortcut': 'There is no such shortcut saved: ',
    'created_shortcut_exists':
    'Shortcut is already in the database. Try "update" command.',
    'no_data': 'There are no shortcuts saved. Try "create" or "help" command.',
}


class CommandLine:
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
            sys.exit(MSG['empty'])

    def command_args(self):
        """
        Check if the command is valid;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        command = self.arguments[0]
        Validators.command(available_cmds=self.commands, command=command)
        Command().valid[command](args=self.arguments, data=self.data)
        return tuple(self.arguments)

    def backup_args(self):
        """
        Check if every argument is a saved shortcut;
            if not: raise SystemExit
            else: return tuple with valid arg
        """
        for arg in self.arguments:
            Validators.shortcut(args=arg, datapath=self.data)
        return (None, ) + tuple(self.arguments)


class Command:
    """
    Check that the command has correct arguments;
        if not: raise SystemExit with the relevant message.
    """
    def __init__(self):
        self.valid = {
            'create':
            lambda args, data: all([
                len(args) >= 4,
                Validators.created_shortcut_exists(args=args[1], datapath=data)
            ]),
            'update':
            lambda args, data: all([
                len(args) == 2,
                Validators.shortcut(args=args[1], datapath=data)
            ]),
            'delete':
            lambda args, data: all([
                len(args) == 2,
                Validators.shortcut(args=args[1], datapath=data)
            ]),
            # TODO: show all that exist
            'show':
            lambda args, data: all([len(args) >= 2] + [
                Validators.shortcut(args=arg, datapath=data)
                for arg in args[1:]
            ]),
            'showall':
            lambda args, data: all([
                len(args) == 1,
                Validators.data_not_empty(datapath=data), args[0] == 'showall'
            ]),
        }


class Validators:
    # TODO: something's wrong!
    """
    db_connect:
        wrapper(args, datapath) -> func(db_cursor, args=tulple())
    """
    @db_connect
    def created_shortcut_exists(shortcut, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if exists:
            sys.exit(MSG['created_shortcut_exists'])

    @db_connect
    def shortcut(shortcut, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if not exists:
            sys.exit(MSG['invalid_shortcut'] + shortcut)

    @db_connect
    def data_not_empty(db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS (SELECT * FROM shortcuts)''')
        exists = selection.fetchone()[0]
        if not exists:
            sys.exit(MSG['no_data'])

    def command(command, available_cmds):
        if command in available_cmds:
            return True
        sys.exit(MSG['invalid_cmd'] + command)


class DirPaths:
    pass

if __name__ == '__main__':
    Command().valid['create'](args=['create','NAME','a','b'], data='test.db')
    Command().valid['delete'](args=['delete','NAME'], data='test.db')
    Command().valid['show'](args=['show','TEST','NAME'], data='test.db')
