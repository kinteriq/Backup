import pytest
import os

import check
import commands
import outputs
from constants import SHORTCUT_NAMES


# TODO add all commands tests
COMMANDS = commands.COMMANDS


class TestCommandLineComplete:
    @staticmethod
    def test_check_no_args(empty_db_cursor, DB_PATH):
        with pytest.raises(SystemExit) as e:
            check.CommandLine(datapath=DB_PATH,
                              arguments=[],
                              all_commands=COMMANDS).complete()
        assert outputs.COMMANDS_INFO.rstrip() in e.exconly()

    @staticmethod
    # TODO refactor
    def test_check_invalid_backup_args_and_invalid_cmd(empty_db_cursor, DB_PATH):
        args = ['wrong1', 'wrong2', 'wrong3']
        with pytest.raises(SystemExit) as e:
            check.CommandLine(datapath=DB_PATH,
                              arguments=args,
                              all_commands=COMMANDS).complete()
        assert e.exconly().endswith(
            outputs.ERROR_MSG['invalid_cmd'](args[0]))

    @staticmethod
    def test_check_valid_backup_args(mock_fields_db, DB_PATH):
        """
        If all shortcuts are valid - returns a tuple with valid args,
            where the first arg is None, and the rest - shortcut names.
        """
        result = check.CommandLine(datapath=DB_PATH,
                                   arguments=SHORTCUT_NAMES,
                                   all_commands=COMMANDS)

        assert result.complete() == (None, *SHORTCUT_NAMES)

    @staticmethod
    def test_check_invalid_command(empty_db_cursor, DB_PATH):
        command = ['messed', 'up']
        with pytest.raises(SystemExit) as e:
            check.CommandLine(datapath=DB_PATH,
                              arguments=command,
                              all_commands=COMMANDS).complete()
        assert e.exconly().endswith(
            outputs.ERROR_MSG['invalid_cmd'](command[0]))

    @staticmethod
    def test_invalid_show_command_shortcut(empty_db_cursor, DB_PATH):
        name = 'wrong_name'
        with pytest.raises(SystemExit) as e:
            check.CommandLine(datapath=DB_PATH,
                              arguments=['show', name],
                              all_commands=COMMANDS).complete()
        assert e.exconly().endswith(
            outputs.ERROR_MSG['invalid_shortcut'](name))

    @staticmethod
    def test_not_enough_create_command_args(empty_db_cursor, DB_PATH):
        args = ('create', 'name', 'wrong')
        with pytest.raises(SystemExit) as e:
            check.CommandLine(datapath=DB_PATH,
                              arguments=args,
                              all_commands=COMMANDS).complete()
        assert e.exconly().endswith(
            outputs.ERROR_MSG['invalid_cmd_args'])

    @staticmethod
    def test_created_shortcut_exists(mock_fields_db, DB_PATH):
        with pytest.raises(SystemExit) as e:
            check.CommandLine(
                datapath=DB_PATH,
                arguments=['create', SHORTCUT_NAMES[0], '1/path', '2/path'],
                all_commands=COMMANDS).complete()
        assert e.exconly().endswith(
            outputs.ERROR_MSG['created_shortcut_exists'])

    @staticmethod
    def test_valid_command(empty_db_cursor, DB_PATH):
        """
        Test a function returns a non-empty tuple upon receiving a valid command
        """
        args = ('create', 'NAME', 'from/path', 'to/path')
        result = check.CommandLine(datapath=DB_PATH,
                                   arguments=args,
                                   all_commands=COMMANDS)
        assert result.complete() == args

    @staticmethod
    def test_try_showall_with_no_shortcuts_saved(empty_db_cursor, DB_PATH):
        with pytest.raises(SystemExit) as e:
            result = check.CommandLine(datapath=DB_PATH,
                                       arguments=['showall'],
                                       all_commands=COMMANDS).complete()
        assert e.exconly().endswith(outputs.ERROR_MSG['no_data'])

    @staticmethod
    def test_try_showall_with_no_db(DB_PATH):
        with pytest.raises(SystemExit) as e:
            result = check.CommandLine(datapath=DB_PATH,
                                       arguments=['showall'],
                                       all_commands=COMMANDS).complete()
        assert e.exconly().endswith(outputs.ERROR_MSG['no_data'])


class TestPath:
    @staticmethod
    def test_wrong_path():
        path = '/test_backup_wrong_filepath/'
        with pytest.raises(SystemExit) as e:
            check.Path.single(path)
        assert e.exconly().endswith(outputs.ERROR_MSG['wrong_path'](path))

    @staticmethod
    def test_correct_path():
        path = os.getcwd()
        assert check.Path.single(path) == path

    @staticmethod
    def test_auto_expand_path():
        path = '~/'
        assert check.Path.single(path) == os.path.expanduser('~/')
