
class Database:
    def __init__(self):
        self.data = {}

    def add(self, key,value):
        if key in self.data:
            databaseResponse = 'Updated'
        else:
            databaseResponse = 'Added'
        self.data[key] = value
        return databaseResponse

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            databaseResponse ='Deleted'
        else:
            databaseResponse = 'Key not found'
        return databaseResponse
    
    def get(self, key):
        if key in self.data:
            databaseResponse = self.data[key]
        else:
            databaseResponse = ''
        return databaseResponse