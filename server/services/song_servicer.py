from generated import client_services_pb2_grpc
from generated import client_services_pb2
from generated import node_services_pb2_grpc
from generated import node_services_pb2

class SongServicer(client_services_pb2_grpc.ClientServiceServicer):
    def __init__(self, chordNode, strategy, shutdownServerEvent):
        self.chordNode = chordNode
        self.strategy = strategy
        self._shutdownServerEvent = shutdownServerEvent

    def Insert(self, request, context):
        if self.chordNode.isResponsible(request.song):
            domainResponse = self.chordNode.songRepository.put(request.song, request.value)
            if self.chordNode.replicationFactor > 1:
                self.chordNode.replicate(request)
            response = client_services_pb2.InsertResponse(response = domainResponse)
        else:
            response = self.chordNode.successorSongStub.Insert(request)
        return response
    
    def Delete(self, request, context):
        if self.chordNode.isResponsible(request.song):
            domainResponse = self.chordNode.songRepository.put(request.song, '')
            if self.chordNode.replicationFactor > 1:
                self.chordNode.replicate(request)
            response = client_services_pb2.DeleteResponse(response = domainResponse)
        else:
            response = self.chordNode.successorSongStub.Delete(request)
        return response

    def Query(self, request, context):
        if request.song != '*':
            if self.strategy == 'L':
                if self.chordNode.songRepository.contains(request.song) or self.chordNode.isResponsible(request.song):
                    with grpc.insecure_channel(f'{self.chordNode.address.ip}:{self.chordNode.address.port}') as channel:
                        stub = node_services_pb2_grpc.NodeServiceStub(channel)
                        newRequest = node_services_pb2.QueryLinearizabilityRequest(key=request.song) 
                        queryLinearizabilityResponse = stub.QueryLinearizability(newRequest)

                        response = client_services_pb2.QueryResponse()
                        for item in queryLinearizabilityResponse.pairs:
                            pair = client_services_pb2.PairClient(key_entry = item.key_entry, value_entry = item.value_entry)
                            response.pairs.append(pair)
                else:
                    self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query request to {self.chordNode.successor.id}")
                    response = self.chordNode.successorSongStub.Query(request)
                return response
            elif self.strategy == 'E':
                if self.chordNode.songRepository.contains(request.song) or self.chordNode.isResponsible(request.song):
                    domainResponse = self.chordNode.songRepository.getValue(request.song)
                    self.chordNode.logger.debug(f"NODE {self.chordNode.id}: QUERY RESULT {domainResponse}")
                    response = client_services_pb2.QueryResponse() 
                    if domainResponse != '':
                        pair = client_services_pb2.PairClient(key_entry = request.song, value_entry = domainResponse)
                        response.pairs.append(pair)
                else:
                    self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query request to {self.chordNode.successor.id}")
                    response = self.chordNode.successorSongStub.Query(request)
                return response
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-all request to {self.chordNode.successor.id}")
            queryAllRequest = node_services_pb2.QueryAllRequest(id = self.chordNode.id)
            response = self.chordNode.successorNodeStub.QueryAll(queryAllRequest)
                
            foo = client_services_pb2.QueryResponse()
            for item in response.pairs:
                foo.pairs.append(client_services_pb2.PairClient(key_entry = item.key_entry, value_entry = item.value_entry))
            return foo
        
    def Depart(self, request, context):
        # Notify successor of the node that his predecessor changed 
        notifyRequest = node_services_pb2.NotifyRequest(id=self.chordNode.predecessor.id, ip=self.chordNode.predecessor.ip, port = self.chordNode.predecessor.port, neighboor='successor')
        notifyResponse = self.chordNode.successorNodeStub.Notify(request)
        
        # Load Balance: Transfer entries from current node (which is going to depart) to its successor 
        foo = node_services_pb2.LoadBalanceAfterDepartRequest()
        for key,value in self.chordNode.songRepository.database.data.items():
            pair = node_services_pb2.Pair(key_entry = key, value_entry = value)
            foo.pairs.append(pair)
        msg = self.chordNode.successorNodeStub.LoadBalanceAfterDepart(foo)

        # Notify predecessor of the node that his successor changed 
        notifyRequest2 = node_services_pb2.NotifyRequest(id=self.chordNode.successor.id, ip=self.chordNode.successor.ip, port = self.chordNode.successor.port, neighboor ='predecessor')
        notifyResponse2 = self.chordNode.predecessorNodeStub.Notify(notifyRequest2)
        
        self._shutdownServerEvent.set()
        return client_services_pb2.DepartResponse(response='Node {self.chordNode.id} left chord successfully')

    def Overlay(self, request, context):
        self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING overlay request to {self.chordNode.successor.id}")
        overlayAllRequest = node_services_pb2.OverlayAllRequest(id = self.chordNode.id)
        overlayAllResponse = self.chordNode.predecessorNodeStub.OverlayAll(overlayAllRequest)
        response = client_services_pb2.OverlayResponse(ids=overlayAllResponse.ids)
        return response




    