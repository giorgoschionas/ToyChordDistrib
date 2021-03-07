import logging
from concurrent import futures                                                             
import grpc     
import node_messages_pb2
import node_messages_pb2_grpc
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
        try:
            server.wait_for_termination()
        except KeyboardInterrupt:
            # Shuts down the server with 0 seconds of grace period. During the
            # grace period, the server won't accept new connections and allow
            # existing RPCs to continue within the grace period.
            server.stop(0)

    def createTopology(self):
        print("Creating bootstrap node")
        self.predecessor = None  
        self.successor = NeigboorInfo(self.address)      
    
    def join(self, node_id):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = node_messages_pb2_grpc.ChordServiceStub(channel)
            response = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=self.id, ip=self.address.ip, port = self.address.port))
            print("Id of successor " , response.port)
            self.setSuccessor(Address(response.ip, response.port))

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
            self.successor.id
            successorId = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=digest))
            self.deleteKey(key)


    # to request pou pairnei einai to id 
    def FindSuccessor(self, request, context):
        print("Inside successor")
        if self.id == self.successor.id:
            print("Bootstrap node")
            self.setSuccessor(Address(request.ip, request.port))
            return node_messages_pb2.FindSuccessorResponse(id=self.id, ip=self.address.ip, port=self.address.port)
        else:
            if self.between(self.id, request.id, self.successor.id):
                response = node_messages_pb2.FindSuccessorResponse(id=self.successor.id, ip=self.successor.ip, port=self.successor.port)
                self.setSuccessor(Address(request.ip, request.port))
                return response
            else:
                with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
                    print(f"Sending request with data {request.port} from {self.address.port} to {self.successor.port}")
                    stub = node_messages_pb2_grpc.ChordServiceStub(channel)
                    response = stub.FindSuccessor(request)
                    return response

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