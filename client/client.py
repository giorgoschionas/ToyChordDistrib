import grpc
from generated import client_services_pb2
from generated import client_services_pb2_grpc

def run():
  with grpc.insecure_channel('localhost:1024') as channel:
    stub = client_services_pb2_grpc.ClientServiceStub(channel)
    response = stub.Insert(client_services_pb2.InsertRequest(song="karamela5", value='3'))
    print(response.response)


if __name__ == "__main__":
    run()