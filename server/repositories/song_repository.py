from database import database

def between(n1, n2, n3):
    # TODO: added corner case when id == -1
    if n2 == -1:
        return False
    if n1 == -1:
        return True
    # Since it's a circle if n1=n3 then n2 is between
    if n1 < n3:
        return n1 < n2 < n3
    else:
        return n1 < n2 or n2 < n3

class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
    
    def addSong(self, key, value):
        if self.contains(key):
            response = 'Updated'
        else:
            response = 'Added'
        self.database.add(key, value)
        return response

    def deleteSong(self, key):
        if self.contains(key):
            self.database.delete(key)
            response ='Deleted'
        else:
            response = 'Key not found'
        return response

    def getValue(self, key):
        if self.contains(key):
            response = self.database.get(key)
        else:
            response = ''
        return response
    
    def getDHT(self):
        return self.database.data
    
    def contains(self, key):
        return key in self.database.data

    def retrieveSongsLessThan(self, newId, successorId):
        removed_keys = {key : value for key,value in self.database.data.items() if between(hashFunction(key), newId, successorId)}
        for key,_ in removed_keys.items():
            self.database.delete(key)
        return removed_keys