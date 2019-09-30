COMMANDS_INFO = """
COMMANDS:

    ::create a shortcut::
        create NAME PATH_FROM PATH_TO_1 [ PATH_TO_2 ] ...

    ::delete shortcuts::
        delete NAME [ NAME-2 ] ...
    
    ::change shortcut's source and/or destination paths::
        update NAME [ NAME-2 ] ...

    ::fetch shortcut's source and destination paths::
        show NAME [ NAME-2 ] ...

    ::fetch all shortcuts::
        showall

    ::backup::
        NAME
        
    ::delete all shortcuts::
        clear

EXAMPLE:

    ::create a shortcut for later use::
            python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

    ::backup the content of ~/Documents/ to both ~/cloud_1/docs/ and ~/cloud_2/docs/::
            python3 backup.py documents
"""

ERROR_MSG = {
    'invalid_cmd': lambda cmd: f'No such command: "{cmd}".',
    'invalid_cmd_args': 'Invalid command arguments.',
    'invalid_shortcut': lambda s: f'No such shortcut saved: "{s}".',
    'created_shortcut_exists':
    'Shortcut is already in the database. Try "update" command.',
    'no_data': 'No shortcuts saved. Try "create" command.',
    'wrong_path': lambda dir: f'Directory does not exist:\n\t"{dir}".',
}

PROGRAM_END = '====\nDONE.'
PROGRAM_QUIT = '\n=======\nEXIT...'


def create_msg(shortcut):
    return f'Shortcut is created: "{shortcut}".'


def update_msg(shortcut=None, updated_lst=[]):
    start = f'Update "{shortcut}"\n'
    end = f'''Successfully updated: {', '.join(updated_lst)}.'''
    if shortcut and updated_lst:
        return start + end
    if shortcut:
        return start
    return end


def delete_msg(deleted_lst):
    d_string = ', '.join(deleted_lst)
    num = len(deleted_lst)
    return f'Deleted successfully {num} shortcut(s): {d_string}.'


def show_msg(name, source, destinations):
    msg = f'''NAME: {name}
    SOURCE:
        {source}
    DESTINATIONS:
        {destinations}'''
    return msg


def showall_msg(names):
    return 'SAVED NAMES:\n\t' + '\n\t'.join(names)


def clear_msg():
    return 'Database is cleared.'


def copying(source, destination):
    return f'Copying:\n\t{source}\n\t-->{destination}'
