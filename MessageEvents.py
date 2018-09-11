from enum import Enum

class MessageEvents(Enum):
    IDENTIFY = 1
    STATUS = 2
    USERS = 3
    MESSAGE = 4
    PUBLICMESSAGE = 5
    CREATEROOM = 6
    INVITE = 7
    JOINROOM = 8
    ROOMESSAGE = 9
    DISCONNECT = 10

    def __str__(self):
        return{
            'IDENTIFY': "IDENTIFY//",
            'STATUS': "STATUS//",
            'USERS': "USERS//",
            'MESSAGE': "MESSAGE//",
            'PUBLICMESSAGE': "PUBLICMESSAGE//",
            'CREATEROOM': "CREATEROOM//",
            'INVITE': "INVITE//",
            'JOINROOM': "JOINROOM//",
            'ROOMESSAGE': "ROOMESSAGE//",
            'DISCONNECT': "DISCONNECT//"
        }[self.name]
