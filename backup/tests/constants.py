import os


_up_level_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

SHORTCUT_NAMES = ['TEST_1', 'TEST_2']

DB = {
    'name': SHORTCUT_NAMES[0],
    'source': os.path.dirname(__file__),
    'destination': os.path.join(_up_level_dir, 'testBackup1'),
    'another_destination': os.path.join(_up_level_dir, 'testBackup2')
}