
class Database:
    def __init__(self):
        self.data = {}

    def add(self, key,value):
        if key in self.data:
            str = 'Updated'
        else:
            str = 'Added'
        print(str)
        self.data[key] = value
        return str

    def delete(self, key):
        if key in self.data:
            del self.data[key]
            str ='Deleted'
        else:
            str = 'Key not found'
        
        return str
    
    def get(self, key):
        if key in self.data:
            resp = self.data[key]
        else:
            resp = ''
        return resp