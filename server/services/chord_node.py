import logging
from concurrent import futures                                                             
import grpc     
from generated import client_services_pb2
from generated import client_services_pb2_grpc
from generated import node_services_pb2
from generated import node_services_pb2_grpc
import hashlib

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class NeigboorInfo:
    def __init__(self,address):
        self.ip = address.ip
        self.port = address.port
        self.id = sha1(f'{address.ip}:{address.port}')

class ChordNode():
    def __init__(self, address):
        self.id = sha1(f'{address.ip}:{address.port}')
        print('Id of node : ', self.id)
        self.address = address
        self.successor = None
        self.predecessor = None
        self.log = logging.getLogger(__name__)
        self.log.info("Node server listening on %s.", address.ip)
        self.keys = []
        
    def addKey(self,key):
        seplf.keys.append(key)
    
    def deleteKey(self,key):
        self.keys.remove(key)


    def setPredecessor(self, predecessorAddress):
        self.predecessor = NeigboorInfo(predecessorAddress)
    
    def getPredecessor(self):
        return self.predecessor

    def setSuccessor(self, successorAddress):
        self.successor = NeigboorInfo(successorAddress)
    
    def getSuccessor(self):
        return self.successor

    def query(self, key):
        hashed_key = sha1(key)
        if hashed_key in range(self.predecessor, self.id): 
            return database(hashed_key)

    def createTopology(self):
        print("Creating bootstrap node")
        self.predecessor = NeigboorInfo(self.address)  
        self.successor = NeigboorInfo(self.address)      
    
    def join(self, node_id):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.FindSuccessor(node_services_pb2.FindSuccessorRequest(id=self.id, ip=self.address.ip, port = self.address.port))
            print("Id of successor " , response.id)
            self.setSuccessor(Address(response.ip, response.port))
        
        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)

            # Notify successor of new node that his predecessor changed and set the predecessor of new node
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.id, ip=self.address.ip, port = self.address.port))
            self.setPredecessor(Address(response.ip,response.port))
            print("Id of predecessor : ", self.predecessor.id)

            # # Transfer keys that have to be removed from successor of new node to new node
            # new_keys =stub.LoadBalance(node_services_pb2.LoadBalanceRequest(id = self.id))
            # # self.keys = self.keys + new_keys

    def requestSuccessor(self, request):
        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            print(f"Sending request with data {request.port} from {self.address.port} to {self.successor.port}")
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            successorInfo = stub.FindSuccessor(request)
            return successorInfo

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