from enum import Enum

class Events(Enum):
    HANDSHAKE = 1
    MESSAGE = 2
    FILE = 3
    CLOSE = 4

    def __str__(self):
        return{
            'HANDSHAKE' : "HANDSHAKE//",
            'MESSAGE' : "MESSAGE//",
            'FILE' : "FILE//",
            'CLOSE' : "CLOSE//"
        }[self.name]
