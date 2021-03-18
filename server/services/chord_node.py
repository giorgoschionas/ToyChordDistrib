import logging
from concurrent import futures                                                             
import grpc     
import hashlib
import logging

from generated.client_services_pb2 import *
from generated.client_services_pb2_grpc import ClientServiceStub
from generated.node_services_pb2 import *
from generated.node_services_pb2_grpc import NodeServiceStub
from .song_service import SongService
from .node_service import NodeService

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def __eq__(self, other):
        if not isinstance(other, Address):
            return NotImplemented
        return self.ip == other.ip and self.port == other.port

class NeigboorInfo:
    def __init__(self, address):
        self.id = sha1(f'{address.ip}:{address.port}')
        self.address = address
        self._channel = grpc.insecure_channel(f'{self.address.ip}:{self.address.port}')
        self._songStub = ClientServiceStub(self._channel)
        self.songService = SongService(self._songStub)
        self._nodeStub = NodeServiceStub(self._channel)
        self.nodeService = NodeService(self._nodeStub)

class ChordNode:
    def __init__(self, address, replicationFactor, songRepository):
        self.id = sha1(f'{address.ip}:{address.port}')
        self.address = address
        self.successor = None
        self.predecessor = None
        self.replicationFactor = replicationFactor
        self.songRepository = songRepository
        self.logger = logging.getLogger('node')
        self.logger.debug(f'NODE ID: {self.id}')     

    def setPredecessor(self, predecessorAddress):
        if self.predecessor != None:
            self.predecessor._channel.close()
        self.predecessor = NeigboorInfo(predecessorAddress)
        self.logger.debug(f'NODE {self.id}: PREDECESSOR {self.predecessor.id}')        

    def setSuccessor(self, successorAddress):
        if self.successor != None:
            self.successor._channel.close()
        self.successor = NeigboorInfo(successorAddress)
        self.logger.debug(f'NODE {self.id}: SUCCESSOR {self.successor.id}')

    def createTopology(self):
        self.logger.debug("CREATING bootstrap node")
        self.setSuccessor(self.address)
        self.setPredecessor(self.address)
    
    def join(self, bootstrapAddress):
        with grpc.insecure_channel(f'{bootstrapAddress.ip}:{bootstrapAddress.port}') as bootstrapChannel:
            bootstrapNodeStub = NodeServiceStub(bootstrapChannel)
            request = FindSuccessorRequest(id=self.id, ip=self.address.ip, port = self.address.port)
            response = bootstrapNodeStub.FindSuccessor(request)
        self.setSuccessor(Address(response.ip, response.port))

        # Notify successor of new node that his predecessor changed and set the predecessor of new node
        notifyResponse = self.successor.nodeService.notify(self.id, self.address, 'successor')
        self.setPredecessor(Address(notifyResponse.ip, notifyResponse.port))

        # Load Balance: transfer entries from successor of new node to new node
        loadBalanceResponse = self.successor.nodeService.loadBalance(self.id)
        for item in loadBalanceResponse.pairs:
            self.songRepository.addSong(item.key_entry, item.value_entry)

        # Notify predecessor of new node that his successor changed
        notifyPredecessorResponse = self.predecessor.nodeService.notify(self.id, self.address, 'predecessor')
 
    def isResponsible(self, id):
        return self.between(self.predecessor.id, id, self.id)

    def between(self, n1, n2, n3):
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