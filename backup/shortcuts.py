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

from config import DATAPATH
import check
from file_handle import write_to_file


# TODO remove DATAPATH from write_to_file
def create(arguments, data) -> str:
    shortcut, source, *destination = arguments
    check.shortcut_exists(shortcut=shortcut, data=data)
    data[shortcut] = {                          # TODO how to edit json file? without rewrite
        'source': source,
        'destination': destination,
    }
    if data:
        write_to_file(data, path=DATAPATH)
    return f'Shortcut is created: {shortcut}.'


def update(arguments, data):
    for shortcut in arguments:
        print(f'Updating "{shortcut}"')
        source = input('Source: ["enter" to skip]\n')
        destination = input('Destination: ["enter" to skip]\n')
        changed = {'source': source, 'destination': destination}
        for field in changed:
            if not changed[field]:
                continue
            data[shortcut][field] = changed[field]
        if data:
            write_to_file(data, path=DATAPATH)
    return 'Updated successfully.'


def delete(arguments, data):
    deleted = []
    for shortcut in arguments:
        data.pop(shortcut)
        deleted.append(shortcut)
    count = len(deleted)
    deleted_sequence = ', '.join(deleted)
    if data:
        write_to_file(data, path=DATAPATH)
    return f'Successfully deleted {count} shortcut(s): {deleted_sequence}.'


def show(arguments, data):
    output = []
    for shortcut in arguments:
        output.append('\n' + shortcut + ':\n  ' + str(data[shortcut]))
    return ''.join(output) + '\n'


def showall(data, arguments=None):
    all_shortcuts = data.keys()
    return '\n'.join(all_shortcuts)
