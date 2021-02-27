def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  response = stub.SayHello(helloworld_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)
  response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)