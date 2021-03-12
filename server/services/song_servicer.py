from generated import client_services_pb2_grpc
from generated import client_services_pb2
from generated import node_services_pb2_grpc
from generated import node_services_pb2

import grpc
import hashlib

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):
    def __init__(self, chordNode):
        self.chordNode = chordNode

    def Insert(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
            digest = sha1(request.song)
            domainResponse = self.chordNode.songRepository.addSong(digest, request.value)
            return client_services_pb2.InsertResponse(response = domainResponse)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = client_services_pb2_grpc.ClientServiceStub(channel)
                response = stub.Insert(request)
                return response
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.predecessor.id, digest, self.id):
            domainResponse = self.chordNode.songRepository.deleteSong(digest)
            return client_services_pb2.DeleteResponse(response = domainResponse)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = client_services_pb2_grpc.ClientServiceStub(channel)
                response = stub.Delete(request)
                return response

    def Query(self, request, context):
        if request.song != '*':
            digest = sha1(request.song)
            if self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
                domainResponse = self.chordNode.songRepository.getValue(digest)
                foo = client_services_pb2.QueryResponse()
                pair = client_services_pb2.PairClient(key_entry = digest, value_entry = domainResponse)
                foo.pairs.append(pair)
                return foo
            else:
                with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                    stub = client_services_pb2_grpc.ClientServiceStub(channel)
                    response = stub.Query(request)
                    return response
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                response = stub.QueryAll(node_services_pb2.QueryAllRequest(id = self.chordNode.id))
                foo = client_services_pb2.QueryResponse()
                for item in response.pairs:
                    foo.pairs.append(client_services_pb2.PairClient(key_entry = item.key_entry, value_entry = item.value_entry))
                return foo
        
    def Depart(self, request, context):
        pass



    