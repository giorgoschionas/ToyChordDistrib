class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
        self.hashFunction = hashFunction
    
    def addSong(self, song):
        hashedSong = self.hashFunction(song)
        self.database.add(hashedSong)

    def deleteSong(self, song):
        self.database.delete(song)

    def getSong(self, songId):
        return self.database.get(songId)