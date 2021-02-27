import node_messages_pb2_grpc

class ChordServicer(node_messages_pb2_grpc.ChordServiceServicer):
    def __init__(self):
        pass
    
    def Insert(self, request, context):
        response = "Hello"
        return response