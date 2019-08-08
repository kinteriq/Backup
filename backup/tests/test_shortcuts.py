import unittest
from unittest.mock import patch

from backup.shortcuts import Shortcuts


class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.shortcuts = Shortcuts({})
        self.shortcut = 'test'
        self.result = self.shortcuts.create(
            [self.shortcut, 'from/path', 'to/paths'])

    def test_shortcut_is_created(self):
        expected_result = f'Shortcut is created: "{self.shortcut}".'
        self.assertIn(self.shortcut, self.shortcuts.data)
        self.assertEqual(self.result, expected_result)

    def test_show_shortcut(self):
        result = self.shortcuts.show([self.shortcut])
        expected_result = f'{self.shortcut}:\n' +\
            str(self.shortcuts.data[self.shortcut])
        self.assertEqual(result, expected_result)

    user_input = ['changed/path', '']

    @patch('builtins.input', side_effect=user_input)
    def test_update_shortcut(self, user_input):
        self.shortcuts.update([self.shortcut])
        self.assertEqual(self.shortcuts.data[self.shortcut]['source'],
                         'changed/path')
