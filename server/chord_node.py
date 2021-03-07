import logging
from concurrent import futures
import grpc
import node_messages_pb2
import node_messages_pb2_grpc
from chord_servicer import ChordServicer
import hashlib

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest,16)

class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class NeigboorInfo:
    def __init__(self,address):
        self.ip = address.ip
        self.port = address.port
        self.id = sha1(f'{address.ip}:{address.port}')

class ChordNode(node_messages_pb2_grpc.ChordServiceServicer):
    def __init__(self, address):
        self.id = sha1(f'{address.ip}:{address.port}')
        self.address = address
        self.successor = None
        self.predecessor = None
        self.log = logging.getLogger(__name__)
        self.log.info("Node server listening on %s.", address.ip)
        self.keys = []
    
    def addKey(key):
        self.keys.append(key)
    
    def deleteKey(key):
        self.keys.remove(key)


    def setPredecessor(self, predecessorAddress):
        self.predecessor = NeigboorInfo(predecessorAddress)

    def setSuccessor(self, successorAddress):
        self.successor = NeigboorInfo(successorAddress)



    def query(self, key):
        hashed_key = sha1(key)
        if hashed_key in range(self.predecessor, self.id): 
            return database(hashed_key)

    def serve(self):
        port = self.address.port
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        node_messages_pb2_grpc.add_ChordServiceServicer_to_server(self, server)
        server.add_insecure_port(f'[::]:{port}')
        print(f'gRPC server listening on port {port}')
        server.start()
        server.wait_for_termination()
    
    def createTopology(self):
        self.predecessor = None  
        self.successor = NeigboorInfo(self.address)      
    
    def join(self, node_id):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = node_messages_pb2_grpc.ChordServiceStub(channel)
            response = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=self.id))
            print("Id of successor " , response.id)

    def Insert(self, request, context):
        digest = sha1(request.song)
        with grpc.insecure_channel(f'{successor.ip}:{successor.port}') as channel:
            stub = node_messages_pb2_grpc.ChordServiceStub(channel)
            successorInfo = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=digest))
            self.addKey(key)
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        with grpc.insecure_channel(f'{successor.ip}:{successor.port}') as channel:
            stub = node_messages_pb2_grpc.ChordServiceStub(channel)
            successorId = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=digest))
            self.deleteKey(key)


    # to request pou pairnei einai to id 
    def FindSuccessor(self, request, context):
        if self.id == self.successor.id:
            print("Bootstrap node")

            return node_messages_pb2.FindSuccessorResponse(id=self.successor.id)
        else:
            if request.id > self.id and request.id<self.successor.id:
                return node_messages_pb2.FindSuccessorResponse(id=self.successor.id)
            else:
                with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
                    stub = node_messages_pb2_grpc.ChordServiceStub(channel)
                    response = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=request.id))
                    return response







if __name__ == "__main__":
    chord_node = ChordNode(Address(21, 80))