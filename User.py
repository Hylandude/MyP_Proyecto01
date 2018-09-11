from UserStatus import UserStatus

class User():
    def __init__(self, transport):
        self.transport = transport
        self.isAuthenticated = False

    def setName(name):
        self.name = name
        self.isAuthenticated = True
        self.status = UserStatus.ACTIVE

    def setStatus(status):
        if isinstance(status, UserStatus):
            self.status = status
