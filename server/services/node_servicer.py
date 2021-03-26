from services import chord_node
from utilities.network_utilities import Address
from generated.node_services_pb2_grpc import NodeServiceServicer
from generated.node_services_pb2 import *

class NodeServicer(NodeServiceServicer):
    def __init__(self, chordNode):
        self.chordNode = chordNode

    def Notify(self, request, context):
        if request.neighboor == 'successor':
            tempAddr = self.chordNode.predecessor.address
            self.chordNode.setPredecessor(Address(request.ip,request.port))
            return NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)
        else:
            tempAddr = self.chordNode.successor.address
            self.chordNode.setSuccessor(Address(request.ip, request.port))
            return NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)

    def LoadBalanceAfterJoin(self, request, context):
        removedKeys = self.chordNode.songRepository.retrieveSongsLessThan(request.id, self.chordNode.id)
        response = LoadBalanceAfterJoinResponse()
        return self._concatData(response, removedKeys)
    
    def LoadBalanceAfterDepart(self, request, context):
        for item in request.pairs:
            self.chordNode.songRepository.addSong(item.key_entry, item.value_entry)
        return LoadBalanceAfterDepartResponse(msg ='Done')

    def FindSuccessor(self, request, context):
        if self.chordNode.isBootstrap():
            response = FindSuccessorResponse(id=self.chordNode.id, ip=self.chordNode.address.ip, port=self.chordNode.address.port)
        else:
            if self.chordNode.isResponsible(request.id):
                response = FindSuccessorResponse(id=self.chordNode.id, ip=self.chordNode.address.ip, port=self.chordNode.address.port)
            else:
                self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING find-successor request from {self.chordNode.id} to {self.chordNode.successor.id}")
                response = self.chordNode.successor.nodeService.findSuccessor(request.id)
        return response
    

    def QueryAll(self, request, context):
        if request.id == self.chordNode.id:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: QUERY-ALL FINISHED")
            response = QueryAllResponse()
            data = self.chordNode.songRepository.getDHT()
            return self._concatData(response, data)
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-all request to {self.chordNode.successor.id}")
            response = self.chordNode.successor.nodeService.queryAll(request.id)
            data = self.chordNode.songRepository.getDHT()
            # space = {'---','---'}
            # data['---']= '---'
            return self._concatData(response, data)

    def _concatData(self, data, newData):
        for key, value in newData.items():
            pair = Pair(key_entry = key, value_entry = value)
            data.pairs.append(pair)
        return data
    
    def OverlayAll(self, request, context):
        if request.id == self.chordNode.id:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: OVERLAY FINISHED")
            response = OverlayAllResponse()
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING overlay-all request to {self.chordNode.predecessor.id}")
            response = self.chordNode.predecessor.nodeService.overlayAll(request.id)
        response.ids.append(self.chordNode.id)
        return response

    def Replicate(self, request, context):
        if request.k == 0:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: REPLICATE FINISHED")
            response = ReplicateResponse(msg='Successfully replicated entry')
        else:
            self.chordNode.songRepository.put(request.song, request.value)
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING replicate request to {self.chordNode.successor.id}")
            response = self.chordNode.successor.nodeService.replicate(request.k - 1, request.song, request.value)
        return response

    def QueryLinearizability(self, request, context):
        if not self.chordNode.songRepository.contains(request.key):
            response = QueryLinearizabilityResponse(pairs=[])
        else:
            self.chordNode.logger.debug(f"NODE {self.chordNode.id}: SENDING query-linearizability request to {self.chordNode.successor.id}")
            response = self.chordNode.successor.nodeService.queryLinearizability(request.key)
            if len(response.pairs) == 0:
                songValue = self.chordNode.songRepository.getValue(request.key)
                returnPair = Pair(key_entry=request.key, value_entry=songValue)
                response.pairs.append(returnPair)
        return response