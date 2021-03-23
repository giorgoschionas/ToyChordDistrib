import sys
import logging
import threading

from generated import node_services_pb2_grpc, node_services_pb2, client_services_pb2_grpc, client_services_pb2
from repositories.song_repository import SongRepository
from database.database import Database
from services import chord_node, song_servicer, node_servicer
from grpc_server import GrpcServer
from utilities.math_utilities import sha1
from utilities.network_utilities import Address

log = logging.getLogger()

def main(argv):
    # TODO: Find ip from os

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

    BOOTSTRAP_ADDRESS = Address('[2001:648:2ffe:501:cc00:10ff:fead:aa9c]', 2024)

    db = Database()
    songRepository = SongRepository(db, hashFunction=sha1)
    
    address = Address(ip, port)
    newNode = chord_node.ChordNode(address, songRepository)
    nodeServicer = node_servicer.NodeServicer(newNode)

    if address.port == BOOTSTRAP_ADDRESS.port - 1000: 
        newNode.createTopology()
    else:
        newNode.join(BOOTSTRAP_ADDRESS)

    nodeServer = GrpcServer(ip, port + 1000, 100)
    nodeServer.addServicer(nodeServicer, node_services_pb2_grpc.add_NodeServiceServicer_to_server)
    
    songServer = GrpcServer(ip, port, 100)
    songServicer = song_servicer.SongServicer(newNode, k, strategy, songServer.shutdownServerEvent, nodeServer.shutdownServerEvent)
    songServer.addServicer(songServicer, client_services_pb2_grpc.add_ClientServiceServicer_to_server)

    threads = list()
    t1 = threading.Thread(target=nodeServer.run)
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(target=songServer.run)
    t2.start()
    threads.append(t2)

    for t in threads:
        t.join()

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