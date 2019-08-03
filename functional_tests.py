import sys
import unittest
from unittest.mock import patch

from backup import receive_command


class TestCommandLineArgs(unittest.TestCase):
    def test_receive_command(self):
        test_args = [
            'backup.py',
            'create',
            'shortcut_name',
            'path_from',
            'path_to_1',
            'path_to_2'
        ]
        paths_to = set(test_args[4:])
        should_receive = tuple(test_args[1:4] + [ paths_to ])

        with patch.object(sys, 'argv', test_args):
            received = receive_command()

        self.assertEqual(received, should_receive)


if __name__ == '__main__':
    unittest.main()
