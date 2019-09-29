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
from outputs import ERROR_MSG


class Path:
    def single(path):
        if path.startswith('~'):
            path = os.path.join(os.path.expanduser('~'), path[2:])
        if not os.path.exists(path):
            raise SystemExit(ERROR_MSG['wrong_path'](path))
        return path

    def many(paths):
        checked = []
        for p in paths:
            dir_must_exist = os.path.split(p)[0]
            dir_to_be_created = os.path.split(p)[1]      # TODO ask user if create dir
            checked_path = Path.single(dir_must_exist)
            checked.append(os.path.join(checked_path, dir_to_be_created))
        return checked


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

        except sqlite3.OperationalError:
            raise SystemExit(ERROR_MSG['no_data'])

        except SystemExit:
            # see if arg[-s] is [are] a correct command
            valid_args = self.command_args()
        return valid_args

    def empty(self):
        if not self.arguments:
            raise SystemExit(ERROR_MSG['empty'])

    def backup_args(self):
        """
        Check if every argument is a saved shortcut;
            if not: raise SystemExit
            else: return tuple with valid args
        """
        # TODO correct_shortcuts = []
        for arg in self.arguments:
            _Validate.shortcut(args=arg, datapath=self.data)
        return (None, ) + tuple(self.arguments)

    def command_args(self):
        """
        Check if the command is valid;
            if not: raise SystemExit
            else: return tuple with valid args
        """
        command = self.arguments[0]
        _Validate.command(available_cmds=self.commands, command=command)
        if _Validate.cmd_args[command](args=self.arguments, data=self.data):
            return tuple(self.arguments)
        else:
            raise SystemExit(ERROR_MSG['invalid_cmd_args'])


class _Validate:
    cmd_args = {
        'create':
        lambda args, data: not _Validate.created_shortcut_exists(args=args[1],
                                                                datapath=data)
        if len(args) >= 4 else False,
        'update':
        lambda args, data: _Validate.shortcut(args=args[1], datapath=data)
        if len(args) == 2 else False,
        'delete':
        lambda args, data: any([
            len(args) >= 2,
            _Validate.shortcut(args=args[1], datapath=data)
            if len(args) == 2 else False
        ]),
        'show':
        lambda args, data: any([
            len(args) >= 2,
            _Validate.shortcut(args=args[1], datapath=data)
            if len(args) == 2 else False
        ]),
        'showall':
        lambda args, data: _Validate.data_not_empty(datapath=data),
        'clear': lambda args, data: True,
    }

    def command(command, available_cmds):
        if command in available_cmds:
            return True
        raise SystemExit(ERROR_MSG['invalid_cmd'](command))

    @db_connect
    def created_shortcut_exists(shortcut, datapath, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if exists:
            raise SystemExit(ERROR_MSG['created_shortcut_exists'])
        return False

    @db_connect
    def shortcut(shortcut, datapath, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS
            (SELECT 1 FROM shortcuts WHERE name = ?)''', (shortcut, ))
        exists = selection.fetchone()[0]
        if not exists:
            raise SystemExit(ERROR_MSG['invalid_shortcut'](shortcut))
        return True

    @db_connect
    def data_not_empty(args, datapath, db_cursor):
        selection = db_cursor.execute(
            '''SELECT EXISTS (SELECT * FROM shortcuts)''')
        exists = selection.fetchone()[0]
        if not exists:
            raise SystemExit(ERROR_MSG['no_data'])
        return True
