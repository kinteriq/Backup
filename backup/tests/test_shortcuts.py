import pytest

from backup.shortcuts import Shortcuts


class TestShortcuts():
    @classmethod
    def setup_class(self):
        self.data = {}
        self.name = 'NAME'
        self.result = Shortcuts.create(self.data,
            [self.name, 'from/path', 'to/paths'])

    def test_shortcut_is_created(self):
        expected_result = f'Shortcut is created: "{self.name}".'
        assert self.name in self.data
        assert self.result == expected_result

    def test_show_shortcut(self):
        result = Shortcuts.show(self.data, [self.name])
        expected_result = f'{self.name}:\n' +\
            str(self.data[self.name])
        assert result == expected_result

    # def test_update_shortcut(self, monkeypatch):
    #     monkeypatch('builtins.input', ['changed/path', ''])
    #     self.shortcuts.update([self.name])
    #     assert self.shortcuts.data[self.name]['source'] == 'changed/path'
