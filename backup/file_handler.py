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

import json
import sys


def create_json(file: str) -> str:
    with open(file, 'w') as f:
        f.write(json.dumps({}))
    return read_from(file)


def read_from(file: str) -> dict:
    with open(file, 'r') as f:
        file = json.load(f)
    return file

def write_to(file: json, data: dict):
    pass

def get_data():
    try:
        data = read_from('shortcuts.json')
    except FileNotFoundError as exc:
        data = create_json('shortcuts.json')
    else:
        print('DATA FILE COULD NOT BE CREATED')
        sys.exit()
    return data
