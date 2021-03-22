import signal
import logging
import grpc  
import threading
from concurrent import futures

class _Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.address = host + ":" + str(port)
        self.logger = logging.getLogger('server')
        self.shutdownServerEvent = threading.Event()

class GrpcServer(_Server):
    def __init__(self, host, port, maxWorkers=40):
        super().__init__(host, port)
        self.maxWorkers = maxWorkers
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.maxWorkers))
    
    def run(self):
        self.server.add_insecure_port(self.address)
        self.server.start()
        self.logger.info('grpc server is now listening on ' + self.address)
        try:
            # signal.signal(signal.SIGINT, signal.SIG_DFL)
            self.shutdownServerEvent.wait()
            self.server.stop(1)
        except KeyboardInterrupt:
            self.server.stop(0)

    def addServicer(self, servicer, addServicerCallback):
        addServicerCallback(servicer, self.server)
