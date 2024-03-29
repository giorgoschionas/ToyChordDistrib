import logging

from utilities.math_utilities import between
from database import database

class SongRepository:
    def __init__(self, database, hashFunction):
        self.database = database
        self.hashFunction = hashFunction
        self.logger = logging.getLogger('repository')
    
    def put(self, key, value):
        if value == '':
            self.logger.debug(f'DELETING song({key})')
            domainResponse = self.deleteSong(key)
        else:
            self.logger.debug(f'ADDING song({key})')
            domainResponse = self.addSong(key, value)
        return domainResponse

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
        self.logger.debug(f"GETTING song({key})")
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
        removed_keys = {key : value for key,value in self.database.data.items() if between(self.hashFunction(key), newId, successorId)}
        for key,_ in removed_keys.items():
            self.database.delete(key)
        return removed_keys