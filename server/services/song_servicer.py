from generated import client_services_pb2_grpc
from generated import client_services_pb2

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):
    def __init__(self, songRepository):
        self.songRepository = songRepository

    def Insert(self, request, context):
        response = client_services_pb2.InsertResponse(response='Added')
        self.songRepository.add(digest)
        return response

    def Delete(self, request, context):
        domainResponse = self.songRepository.delete(digest)
        if domainResponse == "Success":
            serviceResponse = "Deleted"
        else:
        grpcResponse = client_services_pb2.DeleteResponse(response="An error has occurred")
        return grpcResponse

    def Query(self, request, context):
        if self.songRepository.get(request.song) != None:
            return client_services_pb2.QueryResponse(response='Found', ip=self.ip)
        else:
            return client_services_pb2.QueryResponse(response='Not Found')