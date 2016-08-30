class MockUwsgiInput():
    def __init__(self, content):
        self.content = content
        
    def read(self, length):
        return self.content