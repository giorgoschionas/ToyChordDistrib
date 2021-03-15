
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from ..generated import client_services_pb2
from ..generated import client_services_pb2_grpc
import grpc

VERSION_BANNER = """
CLI application that gives access to a distributed song database based on Chord protocol %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'CLI application that gives access to a distributed song database based on Chord protocol'

        # text displayed at the bottom of --help output
        # epilog = 'Usage: chordy command1 --foo bar'

        # controller level arguments. ex: 'chordy --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    # @ex(
    #     help='example sub command1',

    #     # sub-command level arguments. ex: 'chordy command1 --foo bar'
    #     arguments=[
    #         ### add a sample foo option under subcommand namespace
    #         ( [ '-f', '--foo' ],
    #           { 'help' : 'notorious foo option',
    #             'action'  : 'store',
    #             'dest' : 'foo' } ),
    #     ],
    # )
    # def show(self):
    #     """Example sub-command."""

    #     data = {
    #         'foo' : 'bar',
    #     }

    #     ### do something with arguments
    #     if self.app.pargs.foo is not None:
    #         data['foo'] = self.app.pargs.foo

    #     self.app.render(data, 'command1.jinja2')

    @ex(help='Inserts a new song to the chord dht', 
        # sub-command level arguments. ex: 'chordy command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-k', '--key' ],
              { 'help' : 'song name',
                'required' : 'True',
                'dest' : 'key' } ),
            ( [ '-v', '--value'],
              {
                'help' : 'song value',
                'required' : 'True',
                'dest' : 'value'
              })
        ],
    )
    def insert(self):
        key = self.app.pargs.key
        value = self.app.pargs.value
        with grpc.insecure_channel(f'{self.app.pargs.ip}:{self.app.pargs.port}') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Insert(client_services_pb2.InsertRequest(song=key, value=value))
            print(f'Result: song {key} with value {value} was {response.response}')

    @ex(help='Query a song from the network',
        # sub-command level arguments. ex: 'chordy command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-k', '--key' ],
              { 'help' : 'song name',
                'required' : 'True',
                'dest' : 'key' } )
        ],
    )
    def query(self):
        key = self.app.pargs.key
        with grpc.insecure_channel(f'{self.app.pargs.ip}:{self.app.pargs.port}') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Query(client_services_pb2.QueryRequest(song=key))

            output = []
            headers = ['KEY', 'VALUE']
            for item in response.pairs:
                if not item.value_entry:
                    print(f'Result: song {key} not found')
                    break
                item_list = []
                item_list.append(item.key_entry)
                item_list.append(item.value_entry)
                output.append(item_list)

            self.app.render(output, headers=headers)

    @ex(help='Delete a song from the network',
        # sub-command level arguments. ex: 'chordy command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-k', '--key' ],
              { 'help' : 'song name',
                'required' : 'True',
                'dest' : 'key' } )
        ],
    )
    def delete(self):
        key = self.app.pargs.key
        with grpc.insecure_channel(f'{self.app.pargs.ip}:{self.app.pargs.port}') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Delete(client_services_pb2.DeleteRequest(song=key))
            print(f'Result: song {key} {response.response}')

    @ex(help='Display the topology of the network')
    def overlay(self):
        with grpc.insecure_channel(f'{self.app.pargs.ip}:{self.app.pargs.port}') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Overlay(client_services_pb2.OverlayRequest())
            print('Chord Network topology')
            for item in response.ids:
                print(f'Node id: {item}')

    @ex(help='Leave the chord network')
    def depart(self):
        with grpc.insecure_channel(f'{self.app.pargs.ip}:{self.app.pargs.port}') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Depart(client_services_pb2.DepartRequest())
            print(f'Result: node departed from chord network')