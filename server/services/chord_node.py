import logging
import grpc     

from utilities.math_utilities import sha1, between
from utilities.network_utilities import Address
from generated.client_services_pb2 import *
from generated.client_services_pb2_grpc import ClientServiceStub
from generated.node_services_pb2 import *
from generated.node_services_pb2_grpc import NodeServiceStub
from .song_service import SongService
from .node_service import NodeService

class ChordNode:
    def __init__(self, address):
        self.id = sha1(f'{address.ip}:{address.port}')
        self.address = address
        self.successor = None
        self.predecessor = None
        self._channel = grpc.insecure_channel(f'{self.address.ip}:{self.address.port}')
        self._songStub = ClientServiceStub(self._channel)
        self.songService = SongService(self._songStub)
        self._nodeChannel = grpc.insecure_channel(f'{self.address.ip}:{self.address.port + 1000}')
        self._nodeStub = NodeServiceStub(self._nodeChannel)
        self.nodeService = NodeService(self._nodeStub)
        self.logger = logging.getLogger('node')
        self.logger.debug(f'NODE ID: {self.id}')     

    def setPredecessor(self, predecessorAddress):
        if self.predecessor != None:
            self.predecessor._channel.close()
            self.predecessor._nodeChannel.close()
        self.predecessor = ChordNode(predecessorAddress)
        self.logger.debug(f'NODE {self.id}: PREDECESSOR {self.predecessor.id}')        

    def setSuccessor(self, successorAddress):
        if self.successor != None:
            self.successor._channel.close()
            self.successor._nodeChannel.close()
        self.successor = ChordNode(successorAddress)
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
        return between(self.predecessor.id, id, self.id)

    def isBootstrap(self):
        return self.id == self.successor.id


class ExtendedChordNode(ChordNode):
    def __init__(self, address, songRepository):
        super().__init__(address)
        self.songRepository = songRepository