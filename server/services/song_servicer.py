from generated import client_services_pb2_grpc
from generated import client_services_pb2

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):
    def __init__(self, songRepository, chordNode):
        self.songRepository = songRepository
        self.chordNode = chordNode


    def Insert(self, request, context):
        digest = sha1(request.song)
        if self.between(self.predecessor.id, digest, self.id):
            response = client_services_pb2.InsertResponse(response = 'Added')
            self.addKey(digest)
        else:
            chordResponse = self.chordNode.requestSuccessor(digest)
            return chordResponse
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.predecessor.id, digest, self.id):
            self.songRepository.delete(request)
            response = client_services_pb2.DeleteResponse(response ='Deleted')
            self.deleteKey(digest)
        else:
            chordResponse = self.chordNode.requestSuccessor(digest)
            return chordResponse

    
    def Query(self, request, context):
        digest = sha1(request.song)
        if self.between(self.predecessor.id, digest, self.id):
            if digest in self.keys:
                return client_services_pb2.QueryResponse(response = 'Found', ip = self.ip)
            else:
                return client_services_pb2.QueryResponse(response= 'Not Found')
        else:
            chordResponse = self.chordNode.requestSuccessor(digest)
            return chordResponse

    