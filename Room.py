class Room():

    def __init__(self, name):
        self.name = name
        self.connectedUsers = []

    def addUser(self, user):
        self.connectedUsers.append(user)
