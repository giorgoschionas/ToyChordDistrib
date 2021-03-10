import logging

class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.logger = logging.getLogger('grpc_server')
        self.logger.setLevel(logging.INFO)

    def run(self):
        self.logger.info(f"Server is now listening on address {self.ip}:{self.port}")