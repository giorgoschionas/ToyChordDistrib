from concurrent import futures
import grpc
import node_messages_pb2_grpc

from chord_node import ChordNode, Address


def main():
    bootAddress = Address('localhost', 1024)
    nodeAddress = Address('localhost',1025)
    newNode = ChordNode(nodeAddress)
    newNode.serve()
    newNode.join(1)


if __name__ == '__main__':
    main()