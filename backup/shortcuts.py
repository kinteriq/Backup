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


class Shortcuts():
    def create(data, arguments) -> str:
        shortcut, source, *destination = arguments
        if shortcut in data:
            return f'Shortcut exists: "{shortcut}"'
        data[shortcut] = {
            'source': source,
            'destination': destination,
        }
        return f'Shortcut is created: "{shortcut}".'

    def update(data, arguments) -> str:
        for shortcut in arguments:
            print(f'Updating "{shortcut}"')
            source = input('Source: ["enter" to skip]\n')
            destination = input('Destination: ["enter" to skip]\n')
            changed = {'source': source, 'destination': destination}
            for field in changed:
                if not changed[field]:
                    continue
                data[shortcut][field] = changed[field]
        return 'Updated successfully.'

    def delete(data, arguments) -> str:
        deleted = []
        for shortcut in arguments:
            data.pop(shortcut)
            deleted.append(shortcut)
        count = len(deleted)
        deleted_sequence = ', '.join(deleted)
        return f'Successfully deleted {count} shortcut(s): {deleted_sequence}.'

    def show(data, arguments) -> str:
        output = []
        for shortcut in arguments:
            output.append(shortcut + ':\n' + str(data[shortcut]))
        return ''.join(output)

    def showall(self) -> str:
        pass
