import threading
import grpc

from utilities.math_utilities import sha1
from generated.client_services_pb2_grpc import ClientServiceServicer
from generated.client_services_pb2 import *
from generated.node_services_pb2_grpc import NodeServiceStub
from services.node_service import NodeService

class SongServicer(ClientServiceServicer):
    def __init__(self, chordNode, k, strategy, shutdownServerEvent, shutdownServerEvent2):
        self.chordNode = chordNode
        self.replicationFactor = k
        self.strategy = strategy
        self._shutdownServerEvent = shutdownServerEvent
        self._shutdownServerEvent2 = shutdownServerEvent2

    def _getService(self, address):
        nodeChannel = grpc.insecure_channel(f'{address.ip}:{address.port + 1000}')
        nodeStub = NodeServiceStub(nodeChannel)
        nodeService = NodeService(nodeStub)
        return nodeService

    def Insert(self, request, context):
        digest = sha1(request.song)
        nodeAddress = self.chordNode.nodeService.lookup(digest)
        nodeService = self._getService(nodeAddress)
        self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
        if self.strategy == 'L':
            domainResponse = nodeService.replicate(self.replicationFactor, request.song, request.value)
        else:
            task = threading.Thread(target=nodeService.replicate, args=(self.replicationFactor, request.song, request.value,))
            task.start()
        domainResponse = 'Added'
        response = InsertResponse(response=domainResponse)
        return response
    
    def Delete(self, request, context):
        digest = sha1(request.song)
        nodeAddress = self.chordNode.nodeService.lookup(digest)
        nodeService = self._getService(nodeAddress)
        self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
        if self.strategy == 'L':
            nodeService.replicate(self.replicationFactor, request.song, None)
        else:
            task = threading.Thread(target=nodeService.replicate, args=(self.replicationFactor, request.song, None,))
            task.start()
        domainResponse = 'Deleted'
        response = DeleteResponse(response=domainResponse)
        return response

    def Query(self, request, context):
        if request.song != '*':
            nodeAddress = self.chordNode.lookupReplicas(request.song)
            nodeService = self._getService(nodeAddress)
            if self.strategy == 'L':
                queryLinearizabilityResponse = nodeService.queryLinearizability(request.song)
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
        self._shutdownServerEvent2.set()
        return DepartResponse(response='Node {self.chordNode.id} left chord successfully')

    def Overlay(self, request, context):
        self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING overlay request to {self.chordNode.successor.id}")
        overlayAllResponse = self.chordNode.predecessor.nodeService.overlayAll(self.chordNode.id)
        response = OverlayResponse(ids=overlayAllResponse.ids)
        return response




    