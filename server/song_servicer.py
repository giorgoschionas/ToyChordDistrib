import client_services_pb2_grpc
import client_services_pb2

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):

    def Insert(self,request, context):
        digest = sha1(request.song)
        response = client_services_pb2.InsertResponse(response = 'Added')
        self.addKey(digest)