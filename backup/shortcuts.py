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
import sqlite3

import check
from database import db_connect
import outputs


@db_connect
def create(arguments, datapath, db_cursor=None):
    shortcut, source, *destinations = arguments
    checked_source = check.Path.single(source)
    checked_destinations = check.Path.many(destinations)
    format_destinations = ', '.join(checked_destinations)
    values = (shortcut, checked_source, format_destinations)
    db_cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', values)
    print(outputs.create_msg(shortcut))


@db_connect
def update(arguments, datapath, db_cursor=None):
    updated = []
    for shortcut in arguments:
        print(outputs.update_msg(shortcut))
        source = input('- Source ["enter" to skip]:\n')
        destinations = input(
            '- Destinations ["enter" to skip]:\n'
            '*use commas to separate: /user/docs/, /user/temps/\n')
        if source:
            checked_source = check.Path.single(source)
            db_cursor.execute('''UPDATE shortcuts SET source = ?''',
                              (checked_source, ))
        if destinations:
            checked_destinations = check.Path.many(destinations.split(','))
            db_cursor.execute('''UPDATE shortcuts SET destinations = ?''',
                              tuple(checked_destinations))
        if source or destinations:
            updated.append(shortcut)
            print(outputs.update_msg(updated_lst=updated))


@db_connect
def delete(arguments, datapath, db_cursor=None):
    deleted = []
    for shortcut in arguments:
        select_shortcut = db_cursor.execute(
            f'''SELECT * FROM shortcuts WHERE name = ?''', (shortcut, ))
        found_shortcut = select_shortcut.fetchone()
        if found_shortcut is None:
            continue
        db_cursor.execute(f'''DELETE FROM shortcuts WHERE name = ?''',
                          (shortcut, ))
        deleted.append(shortcut)
    print(outputs.delete_msg(deleted))


@db_connect
def show(arguments, datapath, db_cursor=None):
    for shortcut in arguments:
        selection = db_cursor.execute(
            '''SELECT * FROM shortcuts WHERE name = ? ORDER BY name''',
            (shortcut, ))
        for row in selection:
            name, source, destinations = row[0], row[1], row[2]
            print(outputs.show_msg(name, source, destinations))
            

@db_connect
def showall(arguments, datapath, db_cursor=None):
    selection = db_cursor.execute(
        '''SELECT name FROM shortcuts ORDER BY name''')
    print(outputs.showall_msg([row[0] for row in selection]))


@db_connect
def clear(arguments, datapath, db_cursor=None):
    db_cursor.execute('''DROP TABLE IF EXISTS shortcuts''')
    print(outputs.clear_msg())