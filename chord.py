import random 

class Chord:
    def __init__(self, nodes_count, ip, port):
        self.nodes = []
        self.messageQueue = {}

    def join(self, nodeId):
        # check that nodeId does not already exist
        # create node
        newNode = ChordNode(Address('127.0.0.1', 80))

        # check if it is the first node in the network
        if len(self.nodes) == 0:
            pass
            newNode.setPredecessor(new_node.id)
            newNode.setSuccessor(new_node.id) 
        else:
            # ask a random node to tell you your predecessor
            random_node = self.nodes[random.randInt(0, len(self.nodes))]
            response = newNode.send('request', random_node)

            # wait for response
            if response.status == 'Success':
                data = response.getData()
                newNode.setPredecessor(data.nodeId)  
            else:
                print("ΧΑΜΟΣ ΘΑ ΓΙΝΕΙ")
            
            # ask your predecessor for your sucessor and update predecessors successor
            predecessorResponse = newNode.send('request', predecessor)

            # wait for response and update your successor
            if predecessorResponse.status == 'Success':
                data = predecessorResponse.getData()
                newNode.setSuccessor(data.nodeId)  
            else:
                print("ΧΑΜΟΣ ΘΑ ΓΙΝΕΙ")
            
            # inform other nodes that you exist
            self.stabilize()
            
            # request table data that should belong to your hash table
             


