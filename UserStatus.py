from enum import Enum

class MessageEvents(Enum):
    ACTIVE = 1
    AWAY = 2
    BUSY = 3

    def __str__(self):
        return{
            'ACTIVE' : "HANDSHAKE//",
            'AWAY' : "MESSAGE//",
            'BUSY' : "FILE//"
        }[self.name]
