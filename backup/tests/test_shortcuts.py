import pytest
import unittest

from backup import shortcuts


class TestShortcuts():
    def setup_method(self):
        self.name = 'NAME'
        self.result, self.data = shortcuts.create(
            data={}, arguments=[self.name, 'from/path', 'to/paths'])

    def test_shortcut_is_created(self):
        expected_result = f'Shortcut is created: {self.name}.'
        assert self.name in self.data
        assert self.result == expected_result

    def test_update_shortcut(self, monkeypatch):
        with unittest.mock.patch('builtins.input',
                                 side_effect=['changed/path', '']):
            result, data = shortcuts.update(data=self.data,
                                            arguments=[self.name])
        assert data[self.name]['source'] == 'changed/path'

    def test_delete_shortcut(self):
        names = ['TEST', 'NAME']
        expected_result = (f'Successfully deleted {len(names)} shortcut(s): '
                           f'{", ".join(names)}.')
        shortcuts.create(data=self.data, arguments=['TEST', 'path2', 'path3'])
        result, data = shortcuts.delete(data=self.data, arguments=names)
        for shortcut in names:
            assert shortcut not in data
        assert result == expected_result

    def test_show_shortcut(self):
        expected_result = f'\n{self.name}:\n  {str(self.data[self.name])}\n'
        result, _ = shortcuts.show(data=self.data, arguments=[self.name])
        assert result == expected_result

    def test_showall(self):
        shortcuts.create(data=self.data, arguments=['TEST', 'path2', 'path3'])
        expected_result = '\n'.join(self.data.keys())
        result, _ = shortcuts.showall(data=self.data)
        assert result == expected_result
