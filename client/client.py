import grpc
import argparse
from cement import App
from controllers.base_controller import *

from generated import client_services_pb2
from generated import client_services_pb2_grpc

class ChordCliApplication(App):
    class Meta:
        label = 'chordy'
        handlers = [
            Base
        ]
        extensions = ['tabulate']
        output_handler = 'tabulate'

with ChordCliApplication() as app:
    try:
        app.run()
    except KeyboardInterrupt as e:
        # do something with e
        app.log.fatal('Caught Exception: %s' % e)
        app.exit_code = 100

# def run():
#     argparse = ArgumentParser(description='CLI application that gives you access to a distributed song database based on chord')

#     parser.add_argument('integers', metavar='N', type=int, nargs='+', help='interger list')
#     parser.add_argument('--sum', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')
#     args = parser.parse_args()

    # with grpc.insecure_channel('localhost:50051') as channel:
    # stub = client_services_pb2_grpc.ClientServiceStub(channel)
    # response = stub.Insert(client_services_pb2.InsertRequest(song="mplas"))
#     print("Greeter client received: ")


# if __name__ == "__main__":
#     run()