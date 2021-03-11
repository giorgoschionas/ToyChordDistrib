from database import database

class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
        self.hashFunction = hashFunction
    
    def addSong(self, song,value):
        hashedSong = self.hashFunction(song)
        response = self.database.add(hashedSong,value)
        return response

    def deleteSong(self, song):
        hashedSong = self.hashFunction(song)
        response = self.database.delete(hashedSong)
        return response

    def getValue(self, song):
        hashedSong = self.hashFunction(song)
        return self.database.get(hashedSong)
    
    def retrieveSongsLessThan(self, id):
        removed_keys = {key : value for key,value in self.database.data.items() if key<=id}
        for key,_ in removed_keys.items():
            self.deleteSong(key)
        return removed_keys