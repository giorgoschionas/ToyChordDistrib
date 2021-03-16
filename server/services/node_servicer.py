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
            self.chordNode.logger.debug(f"Node {self.chordNode.id}: predecessor id {self.chordNode.predecessor.id}")
            return node_services_pb2.NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)
        else:
            tempAddr = self.chordNode.successor
            self.chordNode.setSuccessor(chord_node.Address(request.ip,request.port))
            self.chordNode.logger.debug(f"Node {self.chordNode.id}: successor id {self.chordNode.successor.id}")
            return node_services_pb2.NotifyResponse(ip = tempAddr.ip, port = tempAddr.port)
    
    def LoadBalanceAfterJoin(self, request, context):
        removedKeys = self.chordNode.songRepository.retrieveSongsLessThan(request.id, self.chordNode.id)
        foo = node_services_pb2.LoadBalanceAfterJoinResponse()
        for key, value in removedKeys.items():
            foo.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry = value))
        return foo
    
    def LoadBalanceAfterDepart(self, request, context):
        for item in request.pairs:
            self.chordNode.songRepository.addSong(item.key_entry, item.value_entry)
        return node_services_pb2.LoadBalanceAfterDepartResponse(msg ='Done')


    # to request pou pairnei einai to id 
    def FindSuccessor(self, request, context):
        if self.chordNode.id == self.chordNode.successor.id:
            self.chordNode.logger.debug("Bootstrap node")
            return node_services_pb2.FindSuccessorResponse(id=self.chordNode.id, ip=self.chordNode.address.ip, port=self.chordNode.address.port)
        else:
            if self.chordNode.between(self.chordNode.id, request.id, self.chordNode.successor.id):
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending find-successor request to {self.chordNode.successor.id}")
                response = node_services_pb2.FindSuccessorResponse(id=self.chordNode.successor.id, ip=self.chordNode.successor.ip, port=self.chordNode.successor.port)
                return response
            else:
                return self.chordNode.requestSuccessor(request)
    

    def QueryAll(self, request, context):
        if request.id == self.chordNode.id:
            lastData = self.chordNode.songRepository.getDHT()
            return self._concatData(node_services_pb2.QueryAllResponse(), lastData)
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending query-all request to {self.chordNode.successor.id}")
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                response = stub.QueryAll(request)
                data = self.chordNode.songRepository.getDHT()
                return self._concatData(response, data)

    def _concatData(self, data, newData):
        for key, value in newData.items():
            data.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry = value))
        return data
    
    def OverlayAll(self, request, context):
        if request.id == self.chordNode.id:
            foo = node_services_pb2.OverlayAllResponse()
            foo.ids.append(self.chordNode.id)
            return foo
        else:
            with grpc.insecure_channel(f'{self.chordNode.predecessor.ip}:{self.chordNode.predecessor.port}') as channel:
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending overlay request to {self.chordNode.successor.id}")
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                response = stub.OverlayAll(request)
                response.ids.append(self.chordNode.id)
                return response

    def Replicate(self, request, context):
        if request.k <= 2:
            self.chordNode.logger.debug(f'REPLICATING song({request.song}) to node({self.chordNode.id})')
            self.chordNode.put(request.song, request.value)
            return node_services_pb2.ReplicateResponse(msg='Successfully replicated entry')
        else:
            self.chordNode.put(request.song, request.value)
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}', options=[('grpc.max_send_message_length', int(32e9)), ('grpc.max_receive_message_length', int(32e9)) as channel:
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending replicate request to {self.chordNode.successor.id}")
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                newRequest = node_services_pb2.ReplicateRequest(k = request.k - 1, song = request.song, value = request.value)
                response = stub.Replicate(newRequest)
                return response

    def QueryLinearizability(self, request, context):
        if not self.chordNode.songRepository.contains(request.key):
            return node_services_pb2.QueryLinearizabilityResponse(pairs=[])
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                self.chordNode.logger.debug(f"Node {self.chordNode.id}: sending query-linearizability request to {self.chordNode.successor.id}")
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                newRequest = node_services_pb2.QueryLinearizabilityRequest(key = request.key)
                response = stub.QueryLinearizability(newRequest)
                if len(response.pairs) == 0:
                    songValue = self.chordNode.songRepository.getValue(request.key)
                    returnPair = node_services_pb2.Pair(key_entry = request.key, value_entry = songValue)
                    response.pairs.append(returnPair)
                return response