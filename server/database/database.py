
class Database:
    def __init__(self):
        self.data = {}

    def add(self, key,value):
        self.data[key] = value

    def delete(self, key):
        del self.data[key]
    
    def get(self, key):
        return self.data[key]