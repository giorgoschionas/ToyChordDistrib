import grpc
import node_messages_pb2
import node_messages_pb2_grpc

def run():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = node_messages_pb2_grpc.ChordServiceStub(channel)
    response = stub.Insert(node_messages_pb2.InsertRequest(song="mplas"))
    print("Greeter client received: ")


if __name__ == "__main__":
    run()