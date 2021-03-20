import sys
import os
import logging
import hashlib
import grpc  
from concurrent import futures

from generated import node_services_pb2_grpc, node_services_pb2, client_services_pb2_grpc, client_services_pb2
from repositories.song_repository import SongRepository
from database.database import Database
from services import chord_node, song_servicer, node_servicer
from grpc_server import GrpcServer

log = logging.getLogger()

def sha1(message):
    digest = hashlib.sha1(message.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

def main(argv):
    # TODO: Find ip from os
    # TODO: Get port from args DONE 

    if len(argv) < 4 or len(argv) > 5:
        print('Usage: main.py [ip] [port] [k] {strategy}')
        exit(0)

    ip = argv[1]
    port = int(argv[2])
    k = int(argv[3])

    if len(argv) == 5:
        strategy = argv[4]
    else:
        strategy = 'E'

    BOOTSTRAP_ADDRESS = chord_node.Address('localhost', 1024)

    db = Database()
    songRepository = SongRepository(db, hashFunction=sha1)
    
    address = chord_node.Address(ip, port)
    newNode = chord_node.ChordNode(address, songRepository)
    nodeServicer = node_servicer.NodeServicer(newNode)

    if address == BOOTSTRAP_ADDRESS:
        newNode.createTopology()
    else:
        newNode.join(BOOTSTRAP_ADDRESS)

    nodeServer = GrpcServer(ip, port, maxWorkers=10)
    songServicer = song_servicer.SongServicer(newNode, k, strategy, nodeServer.shutdownServerEvent)
    nodeServer.addServicer(nodeServicer, node_services_pb2_grpc.add_NodeServiceServicer_to_server)
    nodeServer.addServicer(songServicer, client_services_pb2_grpc.add_ClientServiceServicer_to_server)
    nodeServer.run()

    
def setupLogging():
    # only cofnigure logger if script is main module
    # configuring logger in multiple places is bad
    # only top-level module should configure logger
    if not len(log.handlers):
        log.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s: %(asctime)s -- %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)


if __name__ == "__main__":
    setupLogging()
    main(sys.argv)