import sys 
import grpc
from client.generated.client_services_pb2_grpc import ClientServiceStub
from client.generated.client_services_pb2 import *

def main(argv):
    if argv[1] == 'insert':
        with grpc.insecure_channel(f'{argv[2]}:{argv[3]}') as channel:
            stub = ClientServiceStub(channel)
            response = stub.Insert(InsertRequest(song=argv[4], value=argv[5]))
            print(f'Result: song {argv[4]} with value {argv[5]} was {response.response}')
    elif argv[1] == 'query':
        with grpc.insecure_channel(f'{argv[2]}:{argv[3]}') as channel:
            stub = ClientServiceStub(channel)
            response = stub.Insert(QueryRequest(song=argv[4]))
            print(f'Result: song {argv[4]} was {response.pairs.value_entry}')

if __name__ == "__main__":
    main(sys.argv)