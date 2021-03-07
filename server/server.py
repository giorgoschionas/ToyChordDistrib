from concurrent import futures
import grpc
import node_messages_pb2_grpc

from chord_node import ChordNode, Address    

def main():
    bootAddress = Address('localhost', 1024)
    nodeAddress = Address('localhost', 1029)
    newNode = ChordNode(nodeAddress)

    port = nodeAddress.port
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_messages_pb2_grpc.add_ChordServiceServicer_to_server(newNode, server)
    server.add_insecure_port(f'[::]:{port}')
    print(f'gRPC server listening on port {port}')
    server.start()

    newNode.join(1)
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        # Shuts down the server with 0 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        server.stop(0)


if __name__ == '__main__':
    main()