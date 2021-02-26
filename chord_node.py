import logging
from dht import DistributedHashTable

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class ChordNode:
    def __init__(self, address):
        self.id = hash(f'{address.ip}:{address.port}')
        self.address = address
        self.successor = -1
        self.predecessor = -1
        self.dht = DistributedHashTable()
        self.log = logging.getLogger(__name__)
        self.log.info("Node server listening on %s.", address.ip)

    def setPredecessor(self, predecessorId):
        self.predecessor = predecessorId

    def setSuccessor(self, successorId):
        self.successor = successorId


    def query(self, key):
        hashed_key = hash(key)
        if hashed_key in range(self.predecessor, self.id): 
            return database(hashed_key)

if __name__ == "__main__":
    chord_node = ChordNode(Address(21, 80))