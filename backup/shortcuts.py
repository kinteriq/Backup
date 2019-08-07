class Shortcuts():
    def __init__(self, data):
        self.data = data

    def create(self, arguments: list) -> str:
        shortcut, path_from, *paths_to = arguments
        if shortcut in self.data:
            return f'Shortcut exists: "{shortcut}"'
        self.data[shortcut] = {
            'source': path_from,
            'destination': paths_to,
        }
        return f'Shortcut is created: "{shortcut}".'

    def show(self, shortcuts: list) -> str:
        output = []
        for shortcut in shortcuts:
            output.append(shortcut + ':\n' + str(self.data[shortcut]))
        return ''.join(output)

    def update(self, shortcuts: list) -> str:
        for shortcut in shortcuts:
            print(f'Updating "{shortcut}"')
            source = input('Source: ["enter" to skip]\n')
            destination = input('Destination: ["enter" to skip]\n')
            changed = {'source': source, 'destination': destination}
            for field in changed:
                if not changed[field]:
                    continue
                self.data[shortcut][field] = changed[field]

        return 'Updated successfully.'
