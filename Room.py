class Room():

    def __init__(self, name, owner):
        self.name = name
        self.connectedUsers = []
        self.owner = owner

    def addUser(self, user):
        self.connectedUsers.append(user)
