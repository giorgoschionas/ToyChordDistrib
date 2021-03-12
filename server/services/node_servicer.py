from generated import node_services_pb2_grpc, node_services_pb2
from services import chord_node
from repositories import song_repository

import grpc

class NodeServicer(node_services_pb2_grpc.NodeServiceServicer):
    def __init__(self, songRepository, chordNode):
        self.songRepository = songRepository
        self.chordNode = chordNode

    def Notify(self, request, context):
        tempAddr = self.chordNode.getPredecessor()
        self.chordNode.setPredecessor(chord_node.Address(request.ip,request.port))
        print("Id of predecessor : ", self.chordNode.predecessor.id)
        return node_services_pb2.NotifyResponse(ip = tempAddr.ip, port=tempAddr.port)
    
    def LoadBalance(self, request, context):
        removed_keys = self.songRepository.retrieveSongsLessThan(request.id)
        foo = node_services_pb2.LoadBalanceResponse()
        for key,value in removed_keys.items():
            foo.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry=value))
        return foo

    # to request pou pairnei einai to id 
    def FindSuccessor(self, request, context):
        print("Inside successor")
        if self.chordNode.id == self.chordNode.successor.id:
            print("Bootstrap node")
            self.chordNode.setSuccessor(chord_node.Address(request.ip, request.port))
            print("Id of successor : ", self.chordNode.successor.id)
            return node_services_pb2.FindSuccessorResponse(id=self.chordNode.id, ip=self.chordNode.address.ip, port=self.chordNode.address.port)
        else:
            if self.chordNode.between(self.chordNode.id, request.id, self.chordNode.successor.id):
                response = node_services_pb2.FindSuccessorResponse(id=self.chordNode.successor.id, ip=self.chordNode.successor.ip, port=self.chordNode.successor.port)
                self.chordNode.setSuccessor(chord_node.Address(request.ip, request.port))
                print("Id of successor : ", self.chordNode.successor.id)
                return response
            else:
                return self.chordNode.requestSuccessor(request)
    

    def QueryAll(self, request, context):
        if request.id == self.chordNode.id:
            last_data = self.songRepository.getDHT()
            foo = node_services_pb2.QueryAllResponse()
            for key,value in last_data.items():
                foo.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry=value))
            return foo
        else:
            with grpc.insecure_channel(f'{self.chordNode.successor.ip}:{self.chordNode.successor.port}') as channel:
                stub = node_services_pb2_grpc.NodeServiceStub(channel)
                response = stub.QueryAll(request)
                data = self.songRepository.getDHT()
                for key,value in data.items():
                    response.pairs.append(node_services_pb2.Pair(key_entry = key, value_entry=value))
                return response


