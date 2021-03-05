import logging
from concurrent import futures
import grpc
import node_messages_pb2
import node_messages_pb2_grpc
from chord_servicer import ChordServicer



class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

class ChordNode(node_messages_pb2_grpc.ChordServiceServicer):
    def __init__(self, address):
        self.id = int(hash(f'{address.ip}:{address.port}'))
        self.address = address
        self.successor = -1
        self.predecessor = -1
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
        self.successor = self.id      
    
    def join(self, node_id):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = node_messages_pb2_grpc.ChordServiceStub(channel)
            response = stub.FindSuccessor(node_messages_pb2.FindSuccessorRequest(id=str(self.id)))
            print("Id of successor " , response.id)

    def Insert(self, request, context):
        response = "Hello"
        return node_messages_pb2.InsertResponse(response=response)        

    def FindSuccessor(self, request, context):
        if self.id == self.successor:
            print("dsada")

            return node_messages_pb2.FindSuccessorResponse(id=str(self.successor))
        else:
            if int(request.id) > self.id and int(request.id)<self.successor:
                return node_messages_pb2.FindSuccessorResponse(id=self.successor)
            else:
                with grpc.insecure_channel('localhost:1024') as channel:
                    stub = node_messages_pb2_grpc.ChordServiceStub(channel)
                    response = stub.FindSuccessor(node_messages_pb2.FinsSuccessorRequest(id=request.id))
                    return response







if __name__ == "__main__":
    chord_node = ChordNode(Address(21, 80))