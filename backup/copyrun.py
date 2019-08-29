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
import shutil
import sqlite3


def call(shortcuts, path):
    # TODO EOFError KeyboardInterrupt
    for shortcut in shortcuts:
        con = sqlite3.connect(path)
        selection = con.cursor().execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (shortcut, ))
        _copy_manager(selection)
    return True


def _copy_manager(table):
    for row in table:
        source = row[1]
        destinations = row[2].split(', ')
        for d in destinations:
            _copy(source, d, False)


def _copy(source, destination, replace_all):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for file in os.listdir(source):
        path = os.path.join(source, file)
        if os.path.isdir(path):
            destination_dir = os.path.join(destination, file)
            replace_all = _copy(path, destination_dir, replace_all)
        elif os.path.isfile(path):
            destination_file = os.path.join(destination, file)
            # TODO divide
            if os.path.exists(destination_file):
                if replace_all:
                    pass
                else:
                    replace, replace_all = _perm_to_replace(destination_file)
                    if not replace:
                        continue
            print(f'Copying:\n\t{path}\n\t-->{destination_file}')
            shutil.copyfile(path, destination_file)
    return replace_all


def _perm_to_replace(file):
    # TODO: add don't replace all
    _all = False
    ask = input(f'\nFile already exists:\n"{file}"\nReplace (y/all)? ')
    if ask == 'all':
        _all = True
        return (True, _all)
    elif ask == 'y':
        return (True, _all)
    return (False, _all)
