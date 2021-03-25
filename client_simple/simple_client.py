import sys 
import grpc
from generated.client_services_pb2_grpc import ClientServiceStub
from generated.client_services_pb2 import *

def insert(ip, port, key, value):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = ClientServiceStub(channel)
        response = stub.Insert(InsertRequest(song=key, value=value))
        print(f'Result: song {key} with value {value} was {response.response}')

def delete(ip, port, key):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = ClientServiceStub(channel)
        response = stub.Delete(DeleteRequest(song=key))
        print(f'Result: song {key} {response.response}')

def query(ip, port, key):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = ClientServiceStub(channel)
        response = stub.Query(QueryRequest(song=key))
        if len(response.pairs) == 0:
            print(f'Result: song {key} not found')
        else:
            for item in response.pairs:
                print(f'Result: song {item.key_entry} was {item.value_entry}')

def overlay(ip, port):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = ClientServiceStub(channel)
        response = stub.overlay(OverlayRequest())
        print('Chord Network topology')
        for item in response.ids:
            print(f'Node id: {item}') 
        
def depart(ip, port):
    with grpc.insecure_channel(f'{ip}:{port}') as channel:
        stub = ClientServiceStub(channel)
        response = stub.Depart(DepartRequest())
        print(f'Result: node departed from chord network')

#------------------------------------------------------------------------------------------------------------

def main(argv):
    if len(argv) < 3:
        print('Usage: simple_client.py {command} [ip] [port] params')
        exit(0)

    command = argv[1]    

    if command == 'insert':
        if len(argv) != 6:
            print('Usage: simple_client.py insert [ip] [port] [key] [value]')
            exit(0)

        insert(argv[2], argv[3], argv[4], argv[5])
    elif command == 'delete':
        if len(argv) != 5:
            print('Usage: simple_client.py delete [ip] [port] [key]')
            exit(0)

        delete(argv[2], argv[3], argv[4])
    elif command == 'query':
        if len(argv) != 5:
            print('Usage: simple_client.py query [ip] [port] [key]')
            exit(0)

        query(argv[2], argv[3], argv[4])
    elif command == 'overlay':
        if len(argv) != 4:
            print('Usage: simple_client.py overlay [ip] [port]')
            exit(0)

        overlay(argv[2], argv[3])
    elif command == 'depart':
        if len(argv) != 4:
            print('Usage: simple_client.py depart [ip] [port]')
        
        depart(argv[2], argv[3])
    else:
        print('Usage: simple_client.py {command} [ip] [port] params')

if __name__ == "__main__":
    main(sys.argv)