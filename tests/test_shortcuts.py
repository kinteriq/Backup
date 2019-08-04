import unittest

from shortcuts import Shortcuts


class TestShortcuts(unittest.TestCase):
    def setUp(self):
        self.shortcuts = Shortcuts()

    def test_shortcut_is_created(self):
        shortcut = 'test'
        result = self.shortcuts.create(
            shortcut=shortcut,
            path_from='from/path',
            path_to=set(('to/path',))
        )

        expected_result = f'"{shortcut}" shortcut is created.'
        self.assertIn(shortcut, self.shortcuts.data)
        self.assertEqual(result, expected_result)
