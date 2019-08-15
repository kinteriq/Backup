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

import check
import runner
import shortcuts

COMMANDS = {
    'create': shortcuts.create,
    'update': shortcuts.update,
    'delete': shortcuts.delete,
    'show': shortcuts.show,
    'showall': shortcuts.showall,
    'clear': None,
}


def read_from_command_line(data) -> list:
    args = sys.argv[1:]  # exclude 'backup.py'
    check.empty(args)
    check.invalid_shortcut_name(commands=COMMANDS, data=data, arguments=args)
    check.invalid_command(commands=COMMANDS, arguments=args)
    showall_cmd = args[0] == 'showall'
    run_backup_cmd = len(args) == 1 and args[0] in data
    if showall_cmd:
        args = ['showall', None, data]
    elif run_backup_cmd:
        runner.copy_all(shortcut=args[0])
        sys.exit('BACKUP IS FINISHED.')
    return args


def execute_command(command, params, data) -> tuple:
    message, altered_data = COMMANDS[command](arguments=params, data=data)
    return (message, altered_data)
