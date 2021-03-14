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
            domainResponse = self.chordNode.songRepository.addSong(request.song, request.value)
            self.chordNode.replicate(request)
            print(f"INSERT: {domainResponse}")
            return client_services_pb2.InsertResponse(response = domainResponse)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = client_services_pb2_grpc.ClientServiceStub(channel)
                response = stub.Insert(request)
                return response
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.chordNode.predecessor.id, digest, self.id):
            domainResponse = self.chordNode.songRepository.deleteSong(request.song)
            self.chordNode.replicate(request)
            print(f"DELETE: {domainResponse}")
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
                domainResponse = self.chordNode.songRepository.getValue(request.song)
                foo = client_services_pb2.QueryResponse()
                print(f"QUERY: {domainResponse}")
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
                print(f"QUERY ALL: {foo.pairs}")
                return foo
        
    def Depart(self, request, context):
        # Notify successor of the node that his predecessor changed 
        with grpc.insecure_channel(f'{self.successor.ip}:{self.successor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.chordNode.predecessor.id, ip=self.ChordNode.predecessor.ip, port = self.ChordNode.predecessor.port, neighboor='successor'))

            #Load Balance: Transfer entries from current node (which is going to depart) to its successor 
            foo = node_services_pb2.LoadBalanceAfterDepartRequest()
            for key,value in self.chordNode.songRepository.database.data.items():
                foo.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry = value))
            msg = stub.LoadBalanceAfterDepart(foo)

        # Notify predecessor of the node that his successor changed 
        with grpc.insecure_channel(f'{self.predecessor.ip}:{self.predecessor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.chordNode.predecessor.id, ip=self.ChordNode.predecessor.ip, port = self.ChordNode.predecessor.port, neighboor ='predecessor')) 


    def Overlay(self, request, context):
        with grpc.insecure_channel(f'{self.chordNode.predecessor.ip}:{self.chordNode.predecessor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.OverlayAll(node_services_pb2.OverlayAllRequest(id = self.chordNode.id))
            foo = client_services_pb2.OverlayResponse()
            for item in response.ids:
                foo.ids.append(item)
            return foo




    