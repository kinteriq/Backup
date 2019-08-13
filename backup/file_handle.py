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
import os
import sys

from config import DATAPATH


def retreive(file) -> dict:
    try:
        data = read_from(file)
        return data
    except FileNotFoundError:
        create(file)
        data = read_from(file)
        return data


def read_from(file) -> dict:
    with open(file, 'r') as source:
        data = json.load(source)
        return data


def create(file):
    with open(file, 'w') as source:
        source.write(json.dumps({}))


def write_to_file(data: dict, path):
    with open(path, 'w') as source:
        source.write(json.dumps(data))


def get_shortcut_info(shortcut, path):
    data = read_from(path)
    return data[shortcut]


DATABASE = retreive(DATAPATH)
