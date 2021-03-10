import sys
import os
import logging
import hashlib
import grpc  
from concurrent import futures

from generated import node_services_pb2_grpc, client_services_pb2_grpc
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
    ip = "localhost"
    port = int(argv[1])

    db = Database()
    songRepository = SongRepository(db, hashFunction=sha1)
    
    addr = chord_node.Address(ip, port)
    newNode = chord_node.ChordNode(addr)
    nodeServicer = node_servicer.NodeServicer(songRepository, newNode)
    songServicer = song_servicer.SongServicer(songRepository, newNode)

    nodeServer = GrpcServer(ip, port, 10)
    nodeServer.addServicer(nodeServicer, node_services_pb2_grpc.add_NodeServiceServicer_to_server)
    nodeServer.addServicer(songServicer, client_services_pb2_grpc.add_ClientServiceServicer_to_server)

    if port == 1024:
        newNode.createTopology()
    else:
        newNode.join(1)

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
        formatter = logging.Formatter('%(levelname)s: %(asctime)s %(funcName)s(%(lineno)d) -- %(message)s', datefmt = '%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        log.addHandler(ch)

if __name__ == "__main__":
    setupLogging()
    main(sys.argv)