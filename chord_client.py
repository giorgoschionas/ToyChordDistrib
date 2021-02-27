import grpc
import node_messages_pb2
import node_messages_pb2_grpc

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = node_messages_pb2_grpc.ChordServiceStub(channel)
  response = stub.Insert("mplas")
  print("Greeter client received: " + response)


if __name__ == "__main__":
    run()