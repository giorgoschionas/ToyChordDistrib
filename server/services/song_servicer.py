from generated import client_services_pb2_grpc
from generated import client_services_pb2

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):
    def __init__(self, songRepository):
        self.songRepository = songRepository

    def Insert(self, request, context):
        digest = sha1(request.song)
        response = client_services_pb2.InsertResponse(response='Added')
        self.songRepository.add(digest)
        return response

    def Delete(self, request, context):
        digest = sha1(request.song)
        response = client_services_pb2.DeleteResponse(response='Deleted')
        self.songRepository.delete(digest)
        return response

    def Query(self, request, context):
        digest = sha1(request.song)
        if self.songRepository.get(digest) != None:
            return client_services_pb2.QueryResponse(response = 'Found', ip = self.ip)
        else:
            return client_services_pb2.QueryResponse(response= 'Not Found')