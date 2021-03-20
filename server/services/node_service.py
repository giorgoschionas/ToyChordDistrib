from generated.node_services_pb2_grpc import NodeServiceStub
from generated.node_services_pb2 import *

class NodeService:
    def __init__(self, stub : NodeServiceStub):
        self.stub = stub

    def notify(self, id, address, neighboor):
        request = NotifyRequest(id=id, ip=address.ip, port=address.port, neighboor=neighboor)
        return self.stub.Notify(request)

    def loadBalance(self, id):
        request = LoadBalanceAfterJoinRequest(id=id)
        return self.stub.LoadBalanceAfterJoin(request)

    def loadBalanceAfterDepart(self, pairs):
        request = LoadBalanceAfterDepartRequest()
        for key, value in pairs:
            pair = Pair(key_entry=key, value_entry=value)
            request.pairs.append(pair)
        return self.stub.LoadBalanceAfterDepart(request)
    
    def findSuccessor(self, id):
        request = FindSuccessorRequest(id=id)
        return self.stub.FindSuccessor(request)

    def replicate(self, replicationFactor, key, value):
        request = ReplicateRequest(k=replicationFactor, song=key, value=value)
        return self.stub.Replicate(request)

    def overlayAll(self, id):
        request = OverlayAllRequest(id=id)
        return self.stub.OverlayAll(request)

    def queryAll(self, id):
        request = QueryAllRequest(id=id)
        return self.stub.QueryAll(request)

    def queryLinearizability(self, key):
        request = QueryLinearizabilityRequest(key=key)
        return self.stub.QueryLinearizability(request)