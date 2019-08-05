import unittest

from shortcuts import Shortcuts


class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.shortcuts = Shortcuts()

    def test_shortcut_is_created(self):
        shortcut = 'test'
        result = self.shortcuts.create(
        [shortcut,
        'from/path',
        'to/paths']
        )

        expected_result = f'Shortcut is created: "{shortcut}".'
        self.assertIn(shortcut, self.shortcuts.data)
        self.assertEqual(result, expected_result)

    def test_show_shortcut(self):
        shortcut = 'test'

        self.shortcuts.create(
            [shortcut,
            'from/path',
            'to/paths']
        )
        result = self.shortcuts.show([shortcut])
        expected_result = [
            f'{shortcut}:\n' + str(self.shortcuts.data[shortcut])
        ]
        self.assertEqual(result, expected_result)
