class SongRepository:
    def __init__(self, database):
        self.database = database
    
    def addSong(self, song):
        database.add(song)

    def delete(self, song):
        database.delete(song)

    def getSong(self, songId):
        return database.get(songId)