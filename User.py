#!/usr/bin/env python3

from UserStatus import UserStatus

"""
Class that represents an user to be used in the Server
"""
class User():

    """
    Constructor, receives the socket where the client is connected to
    """
    def __init__(self, transport):
        self.transport = transport
        self.isAuthenticated = False
        self.invalidCount = 0
        self.name = ""
        self.pendingInvitations = []

    """
    Function that defines the name upon authentication
    Receives the new name as a string
    """
    def setName(self, name):
        self.name = name
        self.isAuthenticated = True
        self.status = UserStatus.ACTIVE

    """
    Sets the status of the user
    Receives the an UserStatus object
    """
    def setStatus(self, status):
        if isinstance(status, UserStatus):
            self.status = status
