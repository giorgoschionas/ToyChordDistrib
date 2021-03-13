
from cement import Controller, ex
from cement.utils.version import get_version_banner
from ..core.version import get_version

from ..generated import client_services_pb2
from ..generated import client_services_pb2_grpc

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
        epilog = 'Usage: chordy command1 --foo bar'

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


    @ex(
        help='example sub command1',

        # sub-command level arguments. ex: 'chordy command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-f', '--foo' ],
              { 'help' : 'notorious foo option',
                'action'  : 'store',
                'dest' : 'foo' } ),
        ],
    )
    def show(self):
        """Example sub-command."""

        data = {
            'foo' : 'bar',
        }

        ### do something with arguments
        if self.app.pargs.foo is not None:
            data['foo'] = self.app.pargs.foo

        self.app.render(data, 'command1.jinja2')

    @ex(help='Inserts a new song to the chord dht')
    def insert(self, song):
        with grpc.insecure_channel('localhost:1024') as channel:
            stub = client_services_pb2_grpc.ClientServiceStub(channel)
            response = stub.Insert(client_services_pb2.InsertRequest(song="mplas"))

    @ex(help='Query a song from the network')
    def query(self):
        print('Inside query')

    @ex(help='Delete a song from the network')
    def delete(self):
        print('Inside query')
    
    @ex(help='Display the topology of the network')
    def overlay(self):
        print('I')

    @ex(help='Leave the chord network')
    def depart(self, id):
        print('K')
