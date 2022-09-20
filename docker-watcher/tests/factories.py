class FakeContainer:
    def __init__(self, name):
        self.attrs = {
            'Id': '124',
            'Name': name,
            'State': {'Status': 'running', 'Error': 'zzz'}
        }
