from concurrent import futures
import grpc
import node_messages_pb2_grpc
from chord_servicer import ChordServicer
import logging
from signal import signal, SIGTERM

# def main():
#     local_ip = socket.gethostbyname(socket.gethostname())
#     chordy = chord.Chord(10, local_ip, 1024)
#     serve()

def serve():
    port = 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    node_messages_pb2_grpc.add_ChordServiceServicer_to_server(ChordServicer(), server)
    server.add_insecure_port(f'[::]:{port}')
    logging.info(f'gRPC server listening on port {port}')
    server.start()
    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()

def handle_sigterm(*_):
    print("Received shutdown signal")
    all_rpcs_done_event = server.stop(1)
    all_rpcs_done_event.wait()
    print("Shut down gracefully")

if __name__ == '__main__':
    serve()