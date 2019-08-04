class Shortcuts():
    def __init__(self):
        self.data = dict()

    def create(self, shortcut: str, path_from: str, path_to: set) -> str:
        if shortcut in self.data:
            return f'"{shortcut}" is in the database'
        self.data[shortcut] = {
            'original': path_from,
            'destination': path_to,
        }
        return f'"{shortcut}" shortcut is created.'
