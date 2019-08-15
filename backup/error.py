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

MSG = {
    'invalid_cmd': 'There is no such command.',
    'empty': 'Zero arguments provided.',
    'invalid_shortcut_name': 'There is no such shortcut saved.',
    'shortcut_exists': ('Shortcut is already in the database. '
                        'Try "update" command.'),
    'cmd_with_zero_args': ('Command requires arguments. '
                           'Try --help for additional info.'),
}


class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class InvalidCommand(Error):
    def __init__(self):
        super().__init__(message=MSG['invalid_cmd'])


class Empty(Error):
    def __init__(self):
        super().__init__(message=MSG['empty'])


class InvalidShortcutName(Error):
    def __init__(self):
        super().__init__(message=MSG['invalid_shortcut_name'])


class ShortcutExists(Error):
    def __init__(self):
        super().__init__(message=MSG['shortcut_exists'])


class CommandWithZeroArgs(Error):
    def __init__(self):
        super().__init__(message=MSG['cmd_with_zero_args'])
