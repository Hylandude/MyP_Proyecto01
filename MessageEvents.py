#!/usr/bin/env python3

from enum import Enum

"""
Enumeration that represents the events that the server can receive
"""
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

    """
    To String method
    """
    def __str__(self):
        return{
            'IDENTIFY': "IDENTIFY ",
            'STATUS': "STATUS ",
            'USERS': "USERS ",
            'MESSAGE': "MESSAGE ",
            'PUBLICMESSAGE': "PUBLICMESSAGE ",
            'CREATEROOM': "CREATEROOM ",
            'INVITE': "INVITE ",
            'JOINROOM': "JOINROOM ",
            'ROOMESSAGE': "ROOMESSAGE ",
            'DISCONNECT': "DISCONNECT "
        }[self.name]

    """
    Returns a message with the correct syntax for all events
    """
    def validList():
        stringMessage = '''Sintaxis invalida, la sintaxis de los mensajes es:\n
                        \t IDENTIFY nuevoNombre\n
                        \t STATUS status\n
                        \t USERS\n
                        \t MESSAGE destinatario mensaje\n
                        \t PUBLICMESSAGE mensaje\n
                        \t CREATEROOM nombreSala\n
                        \t INVITE nombreSala usuario1 usuario2...\n
                        \t JOINROOM nombreSala\n
                        \t ROOMESSAGE nombreSala mensaje\n
                        \t DISCONNECT'''
        return stringMessage
