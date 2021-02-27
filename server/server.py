import chord 
import grpc
import node_messages_pb2

# def main():
#     local_ip = socket.gethostbyname(socket.gethostname())
#     chordy = chord.Chord(10, local_ip, 1024)
#     serve()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  route_guide_pb2_grpc.add_RouteGuideServicer_to_server(
      RouteGuideServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()