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

from commands import read_from_command_line, execute_command
import config
import database


def main(datapath):
    try:
        database.db_creator(datapath)
    except sqlite3.OperationalError:    # db exists
        pass
    command, *params = read_from_command_line(datapath=datapath)
    execute_command(command=command, params=params, datapath=datapath)


if __name__ == '__main__':
    datapath = config.DATAPATH
    main(datapath=datapath)
