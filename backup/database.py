import functools
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
    Manages the connection with the database which is in the 'datapath' file.
    """
    @functools.wraps(func)
    def wrapper(datapath, args=tuple()):
        connection = sqlite3.connect(datapath)
        cursor = connection.cursor()
        func(args, cursor)
        connection.commit()
        connection.close()

    return wrapper
