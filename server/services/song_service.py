from generated.client_services_pb2 import *
from generated.client_services_pb2_grpc import ClientServiceStub

class SongService:
    def __init__(self, stub: ClientServiceStub):
        self.stub = stub

    def insert(self, key, value):
        request = InsertRequest(song=key, value=value)
        return self.stub.Insert(request)

    def delete(self, key):
        request = DeleteRequest(song=key)
        return self.stub.Delete(request)
    
    def overlay(self):
        request = OverlayRequest()
        return self.stub.Overlay(request)

    def query(self, key):
        request = QueryRequest(song=key)
        return self.stub.Query(request)

    def depart(self, id):
        request = DepartRequest()
        return self.stub.Depart(request)