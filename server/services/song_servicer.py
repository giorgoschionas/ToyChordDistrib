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
    def __init__(self, chordNode, strategy, shutdownServerEvent):
        self.chordNode = chordNode
        self.strategy = strategy
        self._shutdownServerEvent = shutdownServerEvent

    def Insert(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
            domainResponse = self.chordNode.put(request.song, request.value)
            self.chordNode.logger.debug(f'INSERTING song({request.song}) to node({self.chordNode.id})')
            if self.chordNode.replicationFactor > 1:
                self.chordNode.replicate(request)
            return client_services_pb2.InsertResponse(response = domainResponse)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = client_services_pb2_grpc.ClientServiceStub(channel)
                response = stub.Insert(request)
                return response
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
            self.chordNode.logger.debug(f'DELETING song({request.song}) from node({self.chordNode.id})')
            domainResponse = self.chordNode.put(request.song, '')
            if self.chordNode.replicationFactor > 1:
                self.chordNode.replicate(request)
            return client_services_pb2.DeleteResponse(response = domainResponse)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = client_services_pb2_grpc.ClientServiceStub(channel)
                response = stub.Delete(request)
                return response

    def Query(self, request, context):
        if request.song != '*':
            digest = sha1(request.song)
            if self.strategy == 'L':
                if self.chordNode.songRepository.contains(request.song) or self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
                    with grpc.insecure_channel(f'{self.chordNode.address.ip}:{self.chordNode.address.port}') as channel:
                        stub = node_services_pb2_grpc.NodeServiceStub(channel)
                        newRequest = node_services_pb2.QueryLinearizabilityRequest(key=request.song) 
                        response = stub.QueryLinearizability(newRequest)

                        foo = client_services_pb2.QueryResponse()
                        for item in response.pairs:
                            pair = client_services_pb2.PairClient(key_entry = item.key_entry, value_entry = item.value_entry)
                            foo.pairs.append(pair)
                        return foo
                else:
                    with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                        stub = client_services_pb2_grpc.ClientServiceStub(channel)
                        response = stub.Query(request)
                        return response
            elif self.strategy == 'E':
                if self.chordNode.songRepository.contains(request.song) or self.chordNode.between(self.chordNode.predecessor.id, digest, self.chordNode.id):
                    domainResponse = self.chordNode.songRepository.getValue(request.song)
                    self.chordNode.logger.debug(f"Node {self.chordNode.id}: query result {domainResponse}")
                    if domainResponse == '':
                        return client_services_pb2.QueryResponse(pairs=[]) 
                    else:
                        foo = client_services_pb2.QueryResponse()
                        pair = client_services_pb2.PairClient(key_entry = request.song, value_entry = domainResponse)
                        foo.pairs.append(pair)
                        return foo
                else:
                    with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                        self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending query request to {self.chordNode.successor.id}")
                        stub = client_services_pb2_grpc.ClientServiceStub(channel)
                        response = stub.Query(request)
                        return response
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending query-all request to {self.chordNode.successor.id}")
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                response = stub.QueryAll(node_services_pb2.QueryAllRequest(id = self.chordNode.id))
                foo = client_services_pb2.QueryResponse()
                for item in response.pairs:
                    foo.pairs.append(client_services_pb2.PairClient(key_entry = item.key_entry, value_entry = item.value_entry))
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: query-all results {foo.pairs}")
                return foo
        
    def Depart(self, request, context):
        # Notify successor of the node that his predecessor changed 
        with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.chordNode.predecessor.id, ip=self.chordNode.predecessor.ip, port = self.chordNode.predecessor.port, neighboor='successor'))

            #Load Balance: Transfer entries from current node (which is going to depart) to its successor 
            foo = node_services_pb2.LoadBalanceAfterDepartRequest()
            for key,value in self.chordNode.songRepository.database.data.items():
                foo.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry = value))
            msg = stub.LoadBalanceAfterDepart(foo)

        # Notify predecessor of the node that his successor changed 
        with grpc.insecure_channel(f'{self.chordNode.predecessor.ip}:{self.chordNode.predecessor.port}') as channel:
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.Notify(node_services_pb2.NotifyRequest(id=self.chordNode.successor.id, ip=self.chordNode.successor.ip, port = self.chordNode.successor.port, neighboor ='predecessor')) 
        
        self._shutdownServerEvent.set()
        return client_services_pb2.DepartResponse(response='Node {self.chordNode.id} left chord successfully')

    def Overlay(self, request, context):
        with grpc.insecure_channel(f'{self.chordNode.predecessor.ip}:{self.chordNode.predecessor.port}') as channel:
            self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending overlay request to {self.chordNode.successor.id}")
            stub = node_services_pb2_grpc.NodeServiceStub(channel)
            response = stub.OverlayAll(node_services_pb2.OverlayAllRequest(id = self.chordNode.id))
            foo = client_services_pb2.OverlayResponse()
            for item in response.ids:
                foo.ids.append(item)
            return foo




    