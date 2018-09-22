
"""
Class that represents a room to be used in the Server
"""
class Room():
    """
    Room constructor, receives the name of the room and the User object of the owner
    """
    def __init__(self, name, owner):
        self.name = name
        self.connectedUsers = []
        self.owner = owner
    """
    Method to add an user to the room
    Receives the User who will be added
    """
    def addUser(self, user):
        self.connectedUsers.append(user)
