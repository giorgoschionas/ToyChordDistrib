from database import database

class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
        self.hashFunction = hashFunction
    
    def addSong(self, key,value):
        response = self.database.add(key,value)
        return response

    def deleteSong(self, key):
        response = self.database.delete(key)
        return response

    def getValue(self, key):
        return self.database.get(key)
    
    def getDHT(self):
        return self.database.data
    
    def retrieveSongsLessThan(self, id):
        removed_keys = {key : value for key,value in self.database.data.items() if key<=id}
        for key,_ in removed_keys.items():
            self.database.delete(key)
        return removed_keys