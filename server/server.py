import grpc
from concurrent.futures import ThreadPoolExecutor
import node_messages_pb2_grpc
from chord_servicer import ChordServicer

# def main():
#     local_ip = socket.gethostbyname(socket.gethostname())
#     chordy = chord.Chord(10, local_ip, 1024)
#     serve()

def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    node_messages_pb2_grpc.add_ChordServiceServicer_to_server(ChordServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()