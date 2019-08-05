class Shortcuts():
    def __init__(self):
        self.data = dict()

    def create(self, arguments: list) -> str:
        shortcut, path_from, *paths_to = arguments
        if shortcut in self.data:
            return f'Shortcut exists: "{shortcut}"'
        self.data[shortcut] = {
            'original': path_from,
            'destination': paths_to,
        }
        return f'Shortcut is created: "{shortcut}".'

    def show(self, shortcuts: list):
        output = []
        for shortcut in shortcuts:
            output.append(shortcut + ':\n' + str(self.data[shortcut]))
        return output
