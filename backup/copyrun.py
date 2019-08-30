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
            _copy(source, d, False, False)


def _copy(source, destination, replace_all, replace_nothing):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for file in os.listdir(source):
        path = os.path.join(source, file)
        if os.path.isdir(path):
            destination_dir = os.path.join(destination, file)
            replace_all, replace_nothing = _copy(path, destination_dir,
                                                 replace_all, replace_nothing)
        elif os.path.isfile(path):
            destination_file = os.path.join(destination, file)
            replace_one, replace_all, replace_nothing = _replace_manager(
                destination_file, replace_nothing, replace_all)
            if replace_nothing:
                continue
            if replace_all:
                pass
            elif not replace_one:
                continue
            print(f'Copying:\n\t{path}\n\t-->{destination_file}')
            shutil.copyfile(path, destination_file)
    return (replace_all, replace_nothing)


def _replace_manager(destination, replace_nothing, replace_all):
    replace_one = False
    if os.path.exists(destination):
        if replace_nothing or replace_all:
            return (replace_one, replace_all, replace_nothing)
        else:
            replace_one, replace_all, replace_nothing = _perm_to_replace(
                destination)
    return (replace_one, replace_all, replace_nothing)


def _perm_to_replace(file):
    _one = False
    _all = False
    _all_no = False
    ask = input(f'\nFile already exists:\n"{file}"\nReplace (y/all/nothing)? ')
    if ask == 'all':
        _one = True
        _all = True
        return (_one, _all, _all_no)
    elif ask == 'nothing':
        _all_no = True
        return (_one, _all, _all_no)
    elif ask == 'y':
        _one = True
        return (_one, _all, _all_no)
    return (_one, _all, _all_no)
