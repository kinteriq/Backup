import os


_up_level_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..'))

PATH = os.path.join(os.getcwd(), 'test.db')

SHORTCUT_NAMES = ['TEST_1', 'TEST_2']

DESTINATIONS = [
    os.path.join(_up_level_dir, 'testBackup1'),
    os.path.join(_up_level_dir, 'testBackup2'),
    os.path.join(_up_level_dir, 'testBackup3')
]

# DB = {
#     'path': PATH,
#     'name': SHORTCUT_NAMES[0],
#     'second_name': SHORTCUT_NAMES[1],
#     'source': os.path.dirname(__file__),
#     'destination': DESTINATIONS[0],
#     'another_destination': DESTINATIONS[1],
#     'third_destination': DESTINATIONS[2]
# }

DB = {
   'path': PATH,
   'row_1': {
       'name': SHORTCUT_NAMES[0],
       'source': os.path.dirname(__file__),
       'destinations': DESTINATIONS[:2],
   },
   'row_2': {
       'name': SHORTCUT_NAMES[1],
       'source': os.path.dirname(__file__),
       'destinations': DESTINATIONS[2:],
   }
}


class CreateCmd:
    def __init__(self, cmd='create', name=DB['row_1']['name'],
                 source=DB['row_1']['source'],
                 destinations=DB['row_1']['destinations']):
        self.cmd = cmd
        self.name = name
        self.source = source
        self.destinations = destinations
    
    def args(self):
        
        return ['backup.py', self.cmd, self.name, self.source]\
            + self.destinations

    def db_content(self):
        return (self.name, self.source, ', '.join(self.destinations))


class ShowCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(ShowCmd, self).__init__(*args, **kwargs)
        self.cmd = 'show'

    def args(self):
        return ['backup.py', self.cmd, self.name]


class UpdateCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(UpdateCmd, self).__init__(*args, **kwargs)
        self.cmd = 'update'

    def args(self):
        return ['backup.py', self.cmd, self.name]


class ShowallCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(ShowallCmd, self).__init__(*args, **kwargs)
        self.cmd = 'showall'
    
    def args(self):
        return ['backup.py', self.cmd]


class RunbackupCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(RunbackupCmd, self).__init__(*args, **kwargs)
        self.cmd = self.name
    
    def args(self):
        return ['backup.py', self.name]


class DeleteCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(DeleteCmd, self).__init__(*args, **kwargs)
        self.cmd = 'delete'
    
    def args(self):
        return ['backup.py', self.cmd, self.name]


class ClearCmd(CreateCmd):
    def __init__(self, *args, **kwargs):
        super(ClearCmd, self).__init__(*args, **kwargs)
        self.cmd = 'clear'
    
    def args(self):
        return ['backup.py', self.cmd]


VALID_ARGS_WITH_MOCK_DB = [
    ShowCmd().args(),
    ShowallCmd().args(),
    UpdateCmd().args(),
    DeleteCmd().args(),
    ClearCmd().args(),
]


CREATE_1 = CreateCmd(**DB['row_1'])
CREATE_2 = CreateCmd(**DB['row_2'])
