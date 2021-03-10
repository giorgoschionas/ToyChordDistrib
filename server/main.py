import sys
import os
import logging

from generated import node_services_pb2_grpc, client_services_pb2_grpc
from repositories.song_repository import SongRepository
from database.database import Database
from services import chord_node, song_servicer
from grpc_server import GrpcServer

log = logging.getLogger()

def main(argv):
    # TODO: Find ip from os
    # TODO: Get port from args DONE
    ip = "localhost"
    port = argv[1]
    log.debug("Hi")

    db = Database()
    songRepository = SongRepository(db)
    songServicer = song_servicer.SongServicer(songRepository)
    
    # newNode = chord_node.ChordNode()
    nodeServer = GrpcServer(ip, port, 10)
    nodeServer.addServicer(songServicer, client_services_pb2_grpc.add_ClientServiceServicer_to_server)
    nodeServer.run()

    # Thread.run(nodeServer.run())

    # server = Server()
    # add_ClientServiceServicer_to_server(songServicer, server)
    # add_NodeServiceServicer_to_server()
    # Thread.run(server.run())

def setupLogging():
    # only cofnigure logger if script is main module
    # configuring logger in multiple places is bad
    # only top-level module should configure logger
    if not len(log.handlers):
        log.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(funcName)s(%(lineno)d) -- %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)

if __name__ == "__main__":
    setupLogging()
    main(sys.argv)