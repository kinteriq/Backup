import pytest

import backup.shortcuts


class TestShortcuts():
    @classmethod
    def setup_class(self):
        self.data = {}
        self.name = 'NAME'
        self.result = backup.shortcuts.create(data=self.data,
            arguments=[self.name, 'from/path', 'to/paths'])

    def test_shortcut_is_created(self):
        expected_result = f'Shortcut is created: {self.name}.'
        assert self.name in self.data
        assert self.result == expected_result

    def test_show_shortcut(self):
        expected_result = f'\n{self.name}:\n  {str(self.data[self.name])}\n'
        result = backup.shortcuts.show(data=self.data, arguments=[self.name])
        assert result == expected_result

    @pytest.mark.skip('WIP')
    def test_update_shortcut(self, monkeypatch):
        monkeypatch('builtins.input', ['changed/path', ''])
        backup.shortcuts.update(data=self.data, arguments=[self.name])
        assert self.data[self.name]['source'] == 'changed/path'
