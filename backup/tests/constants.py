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

DB = {
    'name': SHORTCUT_NAMES[0],
    'source': os.path.dirname(__file__),
    'destination': DESTINATIONS[0],
    'another_destination': DESTINATIONS[1],
    'third_destination': DESTINATIONS[2]
}


class CreateCmd:
    def __init__(self, cmd='create', name=DB['name'],
                 source=DB['source'], destination=DB['destination'],
                 another_destination=DB['another_destination']):
        self.cmd = cmd
        self.name = name
        self.source = source
        self.destination = destination
        self.destination_2 = another_destination
    
    def args(self):
        return ['backup.py', self.cmd, self.name, self.source,
                self.destination, self.destination_2]

    def db_content(self):
        return (self.name, self.source,
                f'{self.destination}, {self.destination_2}')


class ShowCmd(CreateCmd):
    def __init__(self):
        super().__init__(cmd='show')

    def args(self):
        return ['backup.py', self.cmd, self.name]


class UpdateCmd(CreateCmd):
    def __init__(self):
        super().__init__(cmd='update')

    def args(self):
        return ['backup.py', self.cmd, self.name]


class ShowallCmd(CreateCmd):
    def __init__(self):
        super().__init__(cmd='showall')
    
    def args(self):
        return ['backup.py', self.cmd]


class RunbackupCmd(CreateCmd):
    def __init__(self):
        super().__init__(cmd=CreateCmd().name)
    
    def args(self):
        return ['backup.py', self.name]


class DeleteCmd(CreateCmd):
    def __init__(self):
        super().__init__(cmd='delete')
    
    def args(self):
        return ['backup.py', self.cmd, self.name]