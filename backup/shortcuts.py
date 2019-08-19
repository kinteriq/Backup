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


def db_creator(datapath):
    connection = sqlite3.connect(datapath)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE shortcuts
        (name TEXT PRIMARY KEY, source TEXT, destinations TEXT)''')
    connection.commit()
    connection.close()


def db_connect(func):
    """
    Manages the connection with db, which is inside 'datapath'
    """
    def wrapper(args, datapath):
        connection = sqlite3.connect(datapath)
        cursor = connection.cursor()
        func(args, cursor)
        connection.commit()
        connection.close()

    return wrapper


@db_connect
def create(arguments, db_cursor):
    shortcut, source, *destinations = arguments
    # TODO:
    # check source path
    # check destinations
    format_destinations = ', '.join(destinations)
    values = (shortcut, source, format_destinations)
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
        # TODO:
        # check source path
        # check destinations
        if source:
            db_cursor.execute('''UPDATE shortcuts SET source = ?''',
                              (source, ))
        if destinations:
            db_cursor.execute('''UPDATE shortcuts SET destinations = ?''',
                              (destinations, ))
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


if __name__ == '__main__':
    db_creator('test.db')
    create(['NAME', 'SOURCE', 'DEST', '...'], datapath='test.db')
    create(['TEST', 'SOURCE', 'DEST', '...'], datapath='test.db')
    update(['NAME'], datapath='test.db')
    show(['NAME', 'wrong_NAME', 'TEST'], datapath='test.db')
    showall([], datapath='test.db')
    delete(['NAME', 'wrong_NAME'], datapath='test.db')
    show(['NAME', 'wrong_NAME', 'TEST'], datapath='test.db')
    os.remove('test.db')
