from UserStatus import UserStatus

class User():
    def __init__(self, transport):
        self.transport = transport
        self.isAuthenticated = False
        self.invalidCount = 0
        self.peername =  transport.get_extra_info('sockname')
        self.name = ""
        self.pendingInvitations = []

    def setName(self, name):
        self.name = name
        self.isAuthenticated = True
        self.status = UserStatus.ACTIVE

    def setStatus(self, status):
        if isinstance(status, UserStatus):
            self.status = status
