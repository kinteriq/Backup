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

from commands import read_from_command_line, execute_command
import config
import runner
import file_handle


def main(datapath) -> str:
    data = file_handle.retreive(datapath)
    command, *params = read_from_command_line(data=data)
    if not command:
        runner.copy_all(shortcuts=params, path=datapath)
        sys.exit('BACKUP IS FINISHED.')
    message, altered_data = execute_command(command=command,
                                            params=params,
                                            data=data)
    if altered_data:
        file_handle.write_to_file(data=altered_data, path=datapath)
    return message


if __name__ == '__main__':
    datapath = config.DATAPATH
    print(main(datapath=datapath))
