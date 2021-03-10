import grpc
import client_services_pb2
import client_services_pb2_grpc

def run():
  with grpc.insecure_channel('localhost:50051') as channel:
    stub = client_services_pb2_grpc.ClientServiceStub(channel)
    response = stub.Insert(client_services_pb2.InsertRequest(song="mplas"))
    print("Greeter client received: ")


if __name__ == "__main__":
    run()