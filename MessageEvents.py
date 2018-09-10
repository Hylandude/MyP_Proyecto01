from enum import Enum

class MessageEvents(Enum):
    HANDSHAKE = 1
    MESSAGE = 2
    FILE = 3
    CLOSE = 4
    SERVER = 5

    def __str__(self):
        return{
            'HANDSHAKE' : "HANDSHAKE//",
            'MESSAGE' : "MESSAGE//",
            'FILE' : "FILE//",
            'CLOSE' : "CLOSE//",
            'SERVER' : "SERVER//"
        }[self.name]
