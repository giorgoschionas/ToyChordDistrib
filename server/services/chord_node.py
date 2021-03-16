import logging
from concurrent import futures                                                             
import grpc     
import hashlib
import logging

from generated import client_services_pb2
from generated import client_services_pb2_grpc
from generated import node_services_pb2
from generated import node_services_pb2_grpc

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class NeigboorInfo:
    def __init__(self, address):
        self.id = sha1(f'{address.ip}:{address.port}')
        self.ip = address.ip
        self.port = address.port

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
        self.bootstrapChannel = grpc.insecure_channel('localhost:1024')
        self.bootstrapNodeStub = node_services_pb2_grpc.NodeServiceStub(self.bootstrapChannel)
        self.predecessorChannel = None
        self.successorChannel = None

    def setPredecessor(self, predecessorAddress):
        self.predecessor = NeigboorInfo(predecessorAddress)
        self.logger.debug(f'NODE {self.id}: PREDECESSOR {self.successor.id}')
        if self.predecessorChannel != None:
            self.predecessorChannel.close()
        self.predecessorChannel = grpc.insecure_channel(f'{self.predecessor.ip}:{self.predecessor.port}')
        self.predecessorNodeStub = node_services_pb2_grpc.NodeServiceStub(self.predecessorChannel)
        self.predecessorSongStub = client_services_pb2_grpc.ClientServiceStub(self.predecessorChannel)   
        

    def setSuccessor(self, successorAddress):
        self.successor = NeigboorInfo(successorAddress)
        self.logger.debug(f'NODE {self.id}: SUCCESSOR {self.successor.id}')
        if self.successorChannel != None:
            self.successorChannel.close()
        self.successorChannel = grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}')
        self.successorSongStub = client_services_pb2_grpc.ClientServiceStub(self.successorChannel)
        self.successorNodeStub = node_services_pb2_grpc.NodeServiceStub(self.successorChannel)

    def createTopology(self):
        self.logger.debug("CREATING bootstrap node")
        self.setSuccessor(self.address)
        self.setPredecessor(self.address)
    
    def join(self, nodeId):
        request = node_services_pb2.FindSuccessorRequest(id=self.id, ip=self.address.ip, port = self.address.port)
        response = self.bootstrapNodeStub.FindSuccessor(request)
        self.setSuccessor(Address(response.ip, response.port))

        # Notify successor of new node that his predecessor changed and set the predecessor of new node
        notifyRequest = node_services_pb2.NotifyRequest(id=self.id, ip=self.address.ip, port = self.address.port, neighboor='successor')
        notifyResponse = self.successorNodeStub.Notify(request)
        self.setPredecessor(Address(notifyResponse.ip, notifyResponse.port))

        # Load Balance: transfer entries from successor of new node to new node
        loadBalanceRequest = node_services_pb2.LoadBalanceAfterJoinRequest(id = self.id)
        loadBalanceResponse = self.successorNodeStub.LoadBalanceAfterJoin(loadBalanceRequest)
        for item in loadBalanceResponse.pairs:
            self.songRepository.addSong(item.key_entry, item.value_entry)

        # Notify predecessor of new node that his successor changed
        notifyPredecessorRequest = node_services_pb2.NotifyRequest(id=self.id, ip=self.address.ip, port = self.address.port, neighboor='predecessor')
        notifyPredecessorResponse = self.predecessorNodeStub.Notify(notifyPredecessorRequest)

    def replicate(self, request):
        self.logger.debug(f"NODE {self.id}: SENDING replicate request from {self.id} to {self.successor.id}")
        if type(request) is client_services_pb2.InsertRequest :
            replicateRequest = node_services_pb2.ReplicateRequest(k = self.replicationFactor, song = request.song, value = request.value)
        else:
            replicateRequest = node_services_pb2.ReplicateRequest(k = self.replicationFactor, song = request.song, value = None)
        self.successorNodeStub.Replicate(replicateRequest)
        self.successorChannel.close()

    def isResponsible(self, key):
        digest = sha1(key)
        return self.between(self.predecessor.id, digest, self.id)

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