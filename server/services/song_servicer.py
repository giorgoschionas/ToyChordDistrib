import threading
import grpc
import hashlib

from generated.client_services_pb2_grpc import ClientServiceServicer
from generated.client_services_pb2 import *
from generated.node_services_pb2_grpc import NodeServiceStub

def sha1(msg):
    digest = hashlib.sha1(msg.encode())
    hex_digest= digest.hexdigest()
    return int(hex_digest, 16) % 65536

class SongServicer(ClientServiceServicer):
    def __init__(self, chordNode, k, strategy, shutdownServerEvent):
        self.chordNode = chordNode
        self.replicationFactor = k
        self.strategy = strategy
        self._shutdownServerEvent = shutdownServerEvent

    def Insert(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.isResponsible(digest):
            domainResponse = self.chordNode.songRepository.put(request.song, request.value)
            if self.replicationFactor > 1:
                self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
                if self.strategy == 'L':
                    self.chordNode.successor.nodeService.replicate(self.replicationFactor, request.song, request.value)
                else:
                    task = threading.Thread(target=self.chordNode.successor.nodeService.replicate, args=(self.replicationFactor, request.song, request.value,))
                    task.start()
            response = InsertResponse(response=domainResponse)
        else:
            response = self.chordNode.successor.songService.insert(request.song, request.value)
        return response
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        if self.chordNode.isResponsible(digest):
            domainResponse = self.chordNode.songRepository.put(request.song, '')
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
            if self.replicationFactor > 1:
                if self.strategy == 'L':
                    self.chordNode.successor.nodeService.replicate(self.replicationFactor, request.song, None)
                else:
                    task = threading.Thread(target=self.chordNode.successor.nodeService.replicate, args=(self.replicationFactor, request.song, None,))
                    task.start()
            response = DeleteResponse(response=domainResponse)
        else:
            response = self.chordNode.successor.songService.delete(request.song)
        return response

    def Query(self, request, context):
        if request.song != '*':
            digest = sha1(request.song)
            if self.chordNode.songRepository.contains(request.song) or self.chordNode.isResponsible(digest):
                if self.strategy == 'L':
                    with grpc.insecure_channel(f'{self.chordNode.address.ip}:{self.chordNode.address.port}') as channel:
                        stub = NodeServiceStub(channel)
                        newRequest = QueryLinearizabilityRequest(key=request.song) 
                        queryLinearizabilityResponse = stub.QueryLinearizability(newRequest)

                        response = QueryResponse()
                        for item in queryLinearizabilityResponse.pairs:
                            pair = PairClient(key_entry = item.key_entry, value_entry = item.value_entry)
                            response.pairs.append(pair)
                elif self.strategy == 'E':
                    domainResponse = self.chordNode.songRepository.getValue(request.song)
                    self.chordNode.logger.debug(f"NODE {self.chordNode.id}: QUERY RESULT {domainResponse}")
                    response = QueryResponse() 
                    if domainResponse != '':
                        pair = PairClient(key_entry = request.song, value_entry = domainResponse)
                        response.pairs.append(pair)
            else:
                self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query request to {self.chordNode.successor.id}")
                response = self.chordNode.successor.songService.query(request.song)
            return response
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-all request to {self.chordNode.successor.id}")
            response = self.chordNode.successor.nodeService.queryAll(self.chordNode.id)
                
            foo = QueryResponse()
            for item in response.pairs:
                foo.pairs.append(PairClient(key_entry = item.key_entry, value_entry = item.value_entry))
            return foo
        
    def Depart(self, request, context):
        # Notify successor of the node that his predecessor changed 
        notifyResponse = self.chordNode.successor.nodeService.notify(self.chordNode.predecessor.id, self.chordNode.predecessor.address, 'successor')
        
        # Load Balance: Transfer entries from current node (which is going to depart) to its successor 
        msg = self.chordNode.successor.nodeService.loadBalanceAfterDepart(self.chordNode.songRepository.database.data.items())

        # Notify predecessor of the node that his successor changed 
        notifyPredecessorResponse = self.chordNode.predecessor.nodeService.notify(self.chordNode.successor.id, self.chordNode.successor.address, 'predecessor')
        
        # Send a shutdown event to the server
        self._shutdownServerEvent.set()
        return DepartResponse(response='Node {self.chordNode.id} left chord successfully')

    def Overlay(self, request, context):
        self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING overlay request to {self.chordNode.successor.id}")
        overlayAllResponse = self.chordNode.predecessor.nodeService.overlayAll(self.chordNode.id)
        response = OverlayResponse(ids=overlayAllResponse.ids)
        return response




    