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

import check


def create(arguments, data) -> tuple:
    shortcut, source, *destination = arguments
    check.shortcut_exists(shortcut=shortcut, data=data)
    data[shortcut] = {                          # TODO how to edit json file?
        'source': source,                       # without rewrite
        'destination': destination,
    }
    return (f'Shortcut is created: {shortcut}.', data)


def update(arguments, data) -> tuple:
    for shortcut in arguments:
        print(f'Updating "{shortcut}"')
        source = input('Source: ["enter" to skip]\n')
        destination = input('Destination: ["enter" to skip]\n')
        changed = {'source': source, 'destination': destination}
        for field in changed:
            if not changed[field]:
                continue
            data[shortcut][field] = changed[field]
    return ('Updated successfully.', data)


def delete(arguments, data) -> tuple:
    deleted = []
    for shortcut in arguments:
        data.pop(shortcut)
        deleted.append(shortcut)
    count = len(deleted)
    deleted_sequence = ', '.join(deleted)
    return (f'Successfully deleted {count} shortcut(s): {deleted_sequence}.',
            data)


def show(arguments, data) -> tuple:
    output = []
    for shortcut in arguments:
        output.append('\n' + shortcut + ':\n  ' + str(data[shortcut]))
    return (''.join(output) + '\n', None)


def showall(data, arguments=None) -> tuple:
    all_shortcuts = data.keys()
    return ('\n'.join(all_shortcuts), None)
