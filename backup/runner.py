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

import shutil

import file_handle


def copy_all(shortcuts, path):
    for shortcut in shortcuts:
        paths = file_handle.get_shortcut_paths(shortcut=shortcut,
                                               datapath=path)
        source = paths['source']
        destinations = paths['destination']
        for d_path in destinations:
            print(f'Copying {source} to {d_path}...')
            shutil.copytree(source, d_path)
    return True
