from generated import node_services_pb2_grpc, node_services_pb2
from services import chord_node
from repositories import song_repository

import grpc

class NodeServicer(node_services_pb2_grpc.NodeServiceServicer):
    def __init__(self, chordNode):
        self.chordNode = chordNode

    def Notify(self, request, context):
        if request.neighboor == 'successor':
            tempAddr = self.chordNode.predecessor
            self.chordNode.setPredecessor(chord_node.Address(request.ip,request.port))
            return node_services_pb2.NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)
        else:
            tempAddr = self.chordNode.successor
            self.chordNode.setSuccessor(chord_node.Address(request.ip, request.port))
            return node_services_pb2.NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)
    1;ΧΨΩΒΝ : ΞΠΟΨΔασ
    def LoadBalanceAfterJoin(self, request, context):
        removedKeys = self.chordNode.songRepository.retrieveSongsLessThan(request.id, self.chordNode.id)
        response = node_services_pb2.LoadBalanceAfterJoinResponse()
        return self._concatData(response, removedKeys)
    
    def LoadBalanceAfterDepart(self, request, context):
        for item in request.pairs:
            self.chordNode.songRepository.addSong(item.key_entry, item.value_entry)
        return node_services_pb2.LoadBalanceAfterDepartResponse(msg ='Done')

    # to request pou pairnei einai to id 
    def FindSuccessor(self, request, context):
        if self.chordNode.id == self.chordNode.successor.id:
            response = node_services_pb2.FindSuccessorResponse(id=self.chordNode.id, ip=self.chordNode.address.ip, port=self.chordNode.address.port)
        else:
            if self.chordNode.between(self.chordNode.id, request.id, self.chordNode.successor.id):
                response = node_services_pb2.FindSuccessorResponse(id=self.chordNode.successor.id, ip=self.chordNode.successor.ip, port=self.chordNode.successor.port)
            else:
                self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING find-successor request from {self.chordNode.id} to {self.chordNode.successor.id}")
                response = self.chordNode.successorNodeStub.FindSuccessor(request)
        return response
    

    def QueryAll(self, request, context):
        if request.id == self.chordNode.id:
            self.chordNode.logger.debug("NODE {self.chordNode.id}: QUERY-ALL FINISHED")
            response = node_services_pb2.QueryAllResponse()
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-all request to {self.chordNode.successor.id}")
            response = self.chordNode.successorNodeStub.QueryAll(request)

        data = self.chordNode.songRepository.getDHT()
        return self._concatData(response, data)

    def _concatData(self, data, newData):
        for key, value in newData.items():
            pair = node_services_pb2.Pair(key_entry = key, value_entry = value)
            data.pairs.append(pair)
        return data
    
    def OverlayAll(self, request, context):
        if request.id == self.chordNode.id:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: OVERLAY FINISHED")
            response = node_services_pb2.OverlayAllResponse()
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING overlay-all request to {self.chordNode.predecessor.id}")
            response = self.chordNode.predecessorNodeStub.OverlayAll(request)
        response.ids.append(self.chordNode.id)
        return response

    def Replicate(self, request, context):
        self.chordNode.logger.debug(f'NODE {self.chordNode.id}: REPLICATING song({request.song}) to node({self.chordNode.id})')
        self.chordNode.songRepository.put(request.song, request.value)
        if request.k <= 2:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: REPLICATE FINISHED")
            response = node_services_pb2.ReplicateResponse(msg='Successfully replicated entry')
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
            newRequest = node_services_pb2.ReplicateRequest(k = request.k - 1, song = request.song, value = request.value)
            response = self.chordNode.successorNodeStub.Replicate(newRequest)
        return response

    def QueryLinearizability(self, request, context):
        if not self.chordNode.songRepository.contains(request.key):
            response = node_services_pb2.QueryLinearizabilityResponse(pairs=[])
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-linearizability request to {self.chordNode.successor.id}")
            newRequest = node_services_pb2.QueryLinearizabilityRequest(key = request.key)
            response = self.chordNode.successorNodeStub.QueryLinearizability(newRequest)
            if len(response.pairs) == 0:
                songValue = self.chordNode.songRepository.getValue(request.key)
                returnPair = node_services_pb2.Pair(key_entry = request.key, value_entry = songValue)
                response.pairs.append(returnPair)
        return response