from enum import Enum

class UserStatus(Enum):
    ACTIVE = 1
    AWAY = 2
    BUSY = 3

    def __str__(self):
        return{
            'ACTIVE' : "ACTIVE//",
            'AWAY' : "AWAY//",
            'BUSY' : "BUSY//"
        }[self.name]
