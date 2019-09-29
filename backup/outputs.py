import commands


ERROR_MSG = {
    'invalid_cmd': lambda cmd: f'No such command: "{cmd}". Try "help".',
    'invalid_cmd_args': 'Invalid command arguments. Try "help".',
    'empty': 'Zero arguments provided. Try "help".',
    'invalid_shortcut': lambda s: f'No such shortcut saved: "{s}".',
    'created_shortcut_exists':
    'Shortcut is already in the database. Try "update" command.',
    'no_data': 'No shortcuts saved. Try "create" or "help" command.',
    'wrong_path': lambda dir: f'Directory does not exist:\n\t"{dir}".',
}

COMMANDS_INFO = commands.__doc__
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
