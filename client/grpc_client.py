class GrpcClient:
    def __init__(self):
        self.stubs = {}

    def handle(self):
        pass

    def connect(self, server):
        """
        get server stub
        :param server:
        :return:
        """
        return self.stubs.get(server)

    def load(self, servers):
        """
        load grpc server list
        :param servers: Server
        :return:
        """
        for server in servers:
            channel = grpc.insecure_channel(server.addr)
            stub = service_pb2_grpc.CommonServiceStub(channel)
            self.stubs[server.server] = stub

