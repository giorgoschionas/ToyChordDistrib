import grpc
from generated import client_services_pb2
from generated import client_services_pb2_grpc

def run():
  with grpc.insecure_channel('localhost:1024') as channel:
    stub = client_services_pb2_grpc.ClientServiceStub(channel)
    response = stub.Query(client_services_pb2.QueryRequest(song="milo"))
    print(response.pairs)


if __name__ == "__main__":
    run()