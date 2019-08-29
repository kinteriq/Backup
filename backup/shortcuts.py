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
from database import db_connect, db_creator


@db_connect
def create(arguments, db_cursor):
    shortcut, source, *destinations = arguments
    # TODO: refactor
    checked_source = check.dir_path(source)
    checked_destinations = []
    for d in destinations:
        checked_d = check.dir_path(os.path.split(d)[0])
        checked_destinations.append(
            os.path.join(checked_d,
                         os.path.split(d)[1]))
    format_destinations = ', '.join(checked_destinations)
    values = (shortcut, checked_source, format_destinations)
    db_cursor.execute('''INSERT INTO shortcuts VALUES (?,?,?)''', values)
    print(f'Shortcut is created: "{shortcut}".\n')


@db_connect
def update(arguments, db_cursor):
    for shortcut in arguments:
        print(f'Update "{shortcut}"\n')
        source = input('- Source ["enter" to skip]:\n')
        destinations = input(
            '- Destinations ["enter" to skip]:\n'
            '*use commas to separate: /user/docs/, /user/temps/\n')
        # TODO: refactor
        if source:
            checked_source = check.dir_path(source)
            db_cursor.execute('''UPDATE shortcuts SET source = ?''',
                              (checked_source, ))
        if destinations:
            checked_destinations = []
            for d in destinations.split(','):
                checked_d = check.dir_path(os.path.split(d)[0])
                checked_destinations.append(
                    os.path.join(checked_d,
                                 os.path.split(d)[1]))
            db_cursor.execute('''UPDATE shortcuts SET destinations = ?''',
                              tuple(checked_destinations))
    print('Updated successfully.\n')


@db_connect
def delete(arguments, db_cursor):
    for shortcut in arguments:
        db_cursor.execute(f'''DELETE FROM shortcuts WHERE name = ?''',
                          (shortcut, ))
    print('Deleted successfully.\n')  # TODO add count and list


@db_connect
def show(arguments, db_cursor):
    for shortcut in arguments:
        selection = db_cursor.execute(
            '''SELECT * FROM shortcuts WHERE name = ? ORDER BY name''',
            (shortcut, ))
        for row in selection:
            name, source, destinations = row[0], row[1], row[2]
            print(f'NAME:\n\t{name}\n'
                  f'SOURCE:\n\t{source}\n'
                  f'DESTINATIONS:\n\t{destinations}\n')


@db_connect
def showall(arguments, db_cursor):
    selection = db_cursor.execute(
        '''SELECT name FROM shortcuts ORDER BY name''')
    print('SAVED NAMES:')
    for row in selection:
        print('\t' + row[0])
    print()
