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
"""
COMMANDS:

    ::create a shortcut::
        create NAME PATH_FROM PATH_TO_1 [ PATH_TO_2 ] ...

    ::delete shortcuts::
        delete NAME [ NAME-2 ] ...
    
    ::change shortcut's source and/or destination paths::
        update NAME [ NAME-2 ] ...

    ::fetch shortcut's source and destination paths::
        show NAME [ NAME-2 ] ...

    ::fetch all shortcuts::
        showall

    ::backup::
        NAME
        
    ::delete all shortcuts::
        clear

EXAMPLE:

    ::create a shortcut for later use::
            python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

    ::backup the content of ~/Documents/ to both ~/cloud_1/docs/ and ~/cloud_2/docs/::
            python3 backup.py documents
"""
import sys

import check
import copyrun
import outputs
import shortcuts


COMMANDS = {
    'create': shortcuts.create,
    'update': shortcuts.update,
    'delete': shortcuts.delete,
    'show': shortcuts.show,
    'showall': shortcuts.showall,
    'clear': shortcuts.clear,
}


def read_from_command_line(datapath) -> list:
    args = sys.argv[1:]  # exclude 'backup.py'
    valid_args = check.CommandLine(datapath=datapath,
                                   arguments=args,
                                   all_commands=COMMANDS).complete()
    return valid_args


def execute_command(command, params, datapath):
    if not command:
        try:
            copyrun.call(shortcuts=params, path=datapath)
            raise SystemExit(outputs.PROGRAM_END)
        except KeyboardInterrupt:           # TODO add cleanup
            raise SystemExit(outputs.PROGRAM_QUIT)
        except EOFError:
            raise SystemExit(outputs.PROGRAM_QUIT)
    COMMANDS[command](args=params, datapath=datapath)
