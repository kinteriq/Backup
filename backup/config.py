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

# This is the path to .db file where all shortcuts will be saved
custom_datapath = ''

# Default path to .db file is the directory with this config file
__default_datapath = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'shortcuts.db'))

DATAPATH = custom_datapath or __default_datapath
