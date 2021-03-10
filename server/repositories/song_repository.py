class SongRepository:
    def __init__(self, database):
        self.database = database
    
    def addSong(self, song):
        database.add(song)

    def delete(self, songId):
        database.delete(song)

    def getSong(self, songId):
        database.get(song)