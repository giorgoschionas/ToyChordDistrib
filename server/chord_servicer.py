import node_messages_pb2_grpc
import node_messages_pb2

class ChordServicer(node_messages_pb2_grpc.ChordServiceServicer):
    def __init__(self):
        pass

    def Insert(self, request, context):
        response = "Hello"
        return node_messages_pb2.InsertResponse(response=response)