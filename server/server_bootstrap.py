from concurrent import futures
import grpc
import node_messages_pb2_grpc
from chord_servicer import ChordServicer
from chord_node import ChordNode,Address



def main():
    bootAddress = Address('localhost', 1024)
    bootstrapNode = ChordNode(bootAddress)
    bootstrapNode.createTopology()
    bootstrapNode.serve()


if __name__ == '__main__':
    main()