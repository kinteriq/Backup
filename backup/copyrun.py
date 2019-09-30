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

import outputs


PERMISSIONS = {
        'replace_all': False,
        'replace_nothing': False,
        'replace_one': True,
    }


def call(shortcuts, path):
    con = sqlite3.connect(path)
    for shortcut in shortcuts:
        selection = con.cursor().execute(
            '''SELECT * FROM shortcuts WHERE name = ?''', (shortcut, ))
        try:
            _copy_manager(selection)
        except OSError as e:
            con.close()
            raise SystemExit(e)
    con.close()


def _copy_manager(table):
    for row in table:
        source = row[1]
        destinations = row[2].split(', ')
        for d in destinations:
            _copy(source, d)
    # TODO add check equality


def _copy(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)
    for file in os.listdir(source):
        path = os.path.join(source, file)
        if os.path.isdir(path):
            destination_dir = os.path.join(destination, file)
            _copy(path, destination_dir)
        elif os.path.isfile(path):
            destination_file = os.path.join(destination, file)
            if os.path.exists(destination_file):
                if PERMISSIONS['replace_nothing']:
                    continue
                if PERMISSIONS['replace_all']:
                    pass
                else:
                    _perm_to_replace(destination_file)
                if not PERMISSIONS['replace_one']:
                    continue
            print(outputs.copying(path, destination_file))
            shutil.copyfile(path, destination_file)


def _perm_to_replace(file):
    ask = input(f'''\nFile already exists:
    "{file}"\nReplace (y/all/nothing)? ''')
    if ask == 'all':
        PERMISSIONS['replace_all'] = True
    elif ask == 'nothing':
        PERMISSIONS['replace_one'] = False
        PERMISSIONS['replace_nothing'] = True
    elif ask != 'y':
        PERMISSIONS['replace_one'] = False
    else:
        PERMISSIONS['replace_one'] = True
