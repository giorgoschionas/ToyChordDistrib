class Database:
    def __init__(self):
        self.data = []

    def add(self, song):
        data[song.id] = song

    def delete(self, song):
        data.pop(song)
    
    def get(self, songId):
        return data[songId]