class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
        self.hashFunction = hashFunction
    
    def addSong(self, song):
        hashedSong = self.hashFunction(song)
        database.add(hashedSong)

    def delete(self, song):
        database.delete(song)

    def getSong(self, songId):
        return database.get(songId)