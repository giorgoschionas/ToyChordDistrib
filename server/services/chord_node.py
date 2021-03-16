import logging
from concurrent import futures                                                             
import grpc     
import hashlib
import logging
import time

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
        self.logger.debug(f'Node id: {self.id}')
        
    def setPredecessor(self, predecessorAddress):
        self.predecessor = NeigboorInfo(predecessorAddress)

    def setSuccessor(self, successorAddress):
        self.successor = NeigboorInfo(successorAddress)

    def createTopology(self):
        self.logger.debug("Creating bootstrap node")
        self.predecessor = NeigboorInfo(self.address)  
        self.successor = NeigboorInfo(self.address)      
    
    def join(self, nodeId):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.FindSuccessor(node_services_pb2.FindSuccessorRequest(id=self.id, ip=self.address.ip, port = self.address.port))
            self.setSuccessor(Address(response.ip, response.port))

        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)

            # Notify successor of new node that his predecessor changed and set the predecessor of new node
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.id, ip=self.address.ip, port = self.address.port, neighboor='successor'))
            self.setPredecessor(Address(response.ip,response.port))

            # Load Balance: transfer entries from successor of new node to new node
            retrieved_pairs = stub.LoadBalanceAfterJoin(node_services_pb2.LoadBalanceAfterJoinRequest(id = self.id))
            for item  in retrieved_pairs.pairs:
                self.songRepository.addSong(item.key_entry,item.value_entry)

        with grpc.insecure_channel(f'{self.predecessor.ip}:{self.predecessor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)

            # Notify predecessor of new node that his successor changed
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.id, ip=self.address.ip, port = self.address.port, neighboor='predecessor'))


    
    def requestSuccessor(self, request):
        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            self.logger.debug(f"Node {self.id}: sending find-successor request from {self.address.port} to {self.successor.port}")
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            successorInfo = stub.FindSuccessor(request)
            return successorInfo

    def replicate(self, request):
        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            self.logger.debug(f"Node {self.id}: sending replicate request from {self.address.port} to {self.successor.port}")
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            if type(request) is client_services_pb2.InsertRequest :
                replicateRequest = node_services_pb2.ReplicateRequest(k = self.replicationFactor, song = request.song, value = request.value)
            else:
                replicateRequest = node_services_pb2.ReplicateRequest(k = self.replicationFactor, song = request.song, value = None)
            stub.Replicate(replicateRequest)

    def put(self, key, value):
        if value == '':
            self.logger.debug(f'Node {self.id}: deleting song {key}')
            domainResponse = self.songRepository.deleteSong(key)
        else:
            self.logger.debug(f'Node {self.id}: adding song {key}')
            domainResponse = self.songRepository.addSong(key, value)
        return domainResponse
    
    def get(self, key):
        self.logger.debug(f"Node {self.id}: getting song {key}")
        return self.songRepository.getValue(key)

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