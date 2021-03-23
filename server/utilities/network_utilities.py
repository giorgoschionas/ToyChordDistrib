class Address:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    
    def __eq__(self, other):
        if not isinstance(other, Address):
            return NotImplemented
        return self.ip == other.ip and self.port == other.port