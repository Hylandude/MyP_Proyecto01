#!/usr/bin/env python3

import math
import sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from MessageEvents import MessageEvents
from UserStatus import UserStatus
from User import User
from Room import Room

"""
Server inicialization
Reads port from command line and starts connection
"""
args = sys.argv[1:]
if len(args) != 1:
    print("Usage: $python3 Server.py <port>");
    sys.exit(1)

try:
    port = int(args[0])
except ValueError:
    print("PORT must be an integer number");
    sys.exit(1)

users = []
rooms = {}

address = ("0.0.0.0",port)
server = socket(AF_INET, SOCK_STREAM)
server.bind(address)

buff = 1024

"""
Function to accept all incoming connections.
Launches a new thread for each incoming client
"""
def acceptConnection():
    while True:
        transport, clientAddress = server.accept()
        print("Se recibio una conexion en: "+str(clientAddress))
        Thread(target=listenClient, args=(transport,)).start()

"""
Function that handles incoming data from client
receives the socket that stablished the connection
Creates User object and receives the data from the socket
"""
def listenClient(transport):
    serving = User(transport)
    users.append(serving)
    transportOpen = True;
    while transportOpen:
        try:
            data = transport.recv(buff)
            data_received(data, serving)
        except OSError:
            print("No longer lisening to: "+serving.name)
            transportOpen = False
            serving.transport.close()
            try:
                users.remove(serving)
            except ValueError:
                return

"""
Function that handles incoming MessageEvents
Receives the incoming data as bytes and the user who triggered the event
Uses nested elif to emulate a switch statement
"""
def data_received(data, serving):
    if data:
        data = data.decode()
        incomingString = data
        incomingString = incomingString.replace("\r\n", "")
        incomingData = incomingString.split(" ")
        print("received: "+incomingString+" \nFrom: "+serving.name)
        eventReceived = incomingData[0]
        if validateEvent(eventReceived):
            if eventReceived == "IDENTIFY":
                if len(incomingData) != 2:
                    print ("Invalid IDENTIFY event")
                    notifyInvalidMessage(MessageEvents.validList(), serving)
                else:
                    identify(incomingData[1], serving)
            elif eventReceived == "DISCONNECT":
                if len(incomingData) != 1:
                    print("Invalid DISCONNECT event")
                    notifyInvalidMessage(MessageEvents.validList(), serving)
                else:
                    disconnectUser(serving)
            elif serving.name != "":
                if eventReceived == "STATUS":
                    if len(incomingData) != 2:
                        print("Invalid STATUS event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        status(incomingData[1], serving)
                elif eventReceived == "USERS":
                    if len(incomingData) != 1:
                        print("Invalid USERS event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        sendUserList(serving)
                elif eventReceived == "MESSAGE":
                    if len(incomingData) < 3:
                        print("Invalid MESSAGE event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        personalMessage(incomingData[1], incomingString, serving)
                elif eventReceived == "PUBLICMESSAGE":
                    if len(incomingData) < 2:
                        print("Invalid PUBLICMESSAGE event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        message = incomingString[14:len(incomingString)]
                        msg = messageMaker(message, serving.name, MessageEvents.PUBLICMESSAGE)
                        sendToAll(msg)
                elif eventReceived == "CREATEROOM":
                    print ("CREATEROOM EVENT RECEIVED");
                    if len(incomingData) != 2:
                        print("Invalid CREATEROOM event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        createRoom(incomingData[1], serving)
                elif eventReceived == "INVITE":
                    if len(incomingData) < 3:
                        print("Invalid INVITE event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        invite(incomingData[1], incomingString, serving)
                elif eventReceived == "JOINROOM":
                    if len(incomingData) != 2:
                        print("Invalid JOINROOM event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        joinRoom(incomingData[1], serving)
                elif eventReceived == "ROOMESSAGE":
                    if len(incomingData) < 3:
                        print("Invalid ROOMESSAGE event")
                        notifyInvalidMessage(MessageEvents.validList(), serving)
                    else:
                        roomMessage(incomingData[1], incomingString, serving)

            else:
                print("Usuario no autenticado intento un evento")
                notifyInvalidMessage("No puedes enviar mensajes hasta que te autentiques", serving)

        else:
            print("Se recibio un mensaje invalido")
            notifyInvalidMessage(MessageEvents.validList(), serving)

"""
Function that creates a message string for the client to receive
Return the bytes representation of the message string
"""
def messageMaker(message, author, event, room=""):
    if room != "":
        room = room+"-"
    return (str(event)+room+author+": "+message+"\r\n").encode()

"""
Function that validates if the event received is valid
Receives the event type as a string
Returns true if the event is valid else returns false
"""
def validateEvent(eventType):
    try:
        return eventType+" " == str(MessageEvents[eventType])
    except KeyError:
        return False

"""
Function that sends a message to all connected users
Receives the message to be sent as bytes
"""
def sendToAll(message):
    for user in users:
        try:
            user.transport.send(message)
        except:
            continue

"""
Function to search for an user in the connected users list
Receives the name of the searched user as a string
Returns the User object if found, None if not found
"""
def findUser(searchedName):
    recepient = None
    for user in users:
        if(user.name == searchedName):
            recepient = user
    return recepient

"""
Function that returns a message notifying the user the event sent is invalid
Receives the message to be sent as a string and the User object who triggered the event
"""
def notifyInvalidMessage(notice, serving):
    msg = messageMaker(notice, "[Servidor]", MessageEvents.MESSAGE)
    serving.invalidCount += 1
    serving.transport.send(msg)

"""
Function that handles the IDENTIFY event
Receives the name the user is requesting and the User object who triggered the event
"""
def identify(name, serving):
    if serving.name == "":
        sameNameUser = findUser(name)
        if sameNameUser is None:
            print(name+" se ha conectado")
            msg = messageMaker("Bienvenido: "+name, "[Servidor]", MessageEvents.PUBLICMESSAGE)
            sendToAll(msg)
            serving.setName(name)
        else:
            print("Se recibio un nombre duplicado")
            msg = messageMaker("El nombre que escogiste ya esta en uso", "[Servidor]", MessageEvents.MESSAGE)
            serving.transport.send(msg)
    else:
        print(serving.name+" trato de identificarse dos veces")
        msg = messageMaker("Ya estas identificado, no es posible cambiar tu nombre", "[Servidor]", MessageEvents.MESSAGE)
        serving.transport.send(msg)

"""
Function that handles the STATUS event
Receives the status selected and the User object who triggered the event
"""
def status(statusSelected, serving):
    try:
        serving.setStatus(UserStatus[statusSelected.upper()])
    except KeyError:
        print("Received invalid status on event")
        notifyInvalidMessage("Status invalido. Debe ser 'ACTIVE', 'AWAY' o 'BUSY'", serving)

"""
Function that handles the USERS event
Receives the User object who triggered the event
"""
def sendUserList(serving):
    userString = ""
    for user in users:
        if user.isAuthenticated:
            userString += user.name+", "
    userString = userString[0:len(userString)-2]
    msg = messageMaker(userString, "[Servidor]", MessageEvents.MESSAGE)
    serving.transport.send(msg)

"""
Function that handles the MESSAGE event
Receives the name of the recepient, the whole string that the user sent and the User object who triggered the event
"""
def personalMessage(recepientName, entireString, serving):
    recepient = findUser(recepientName)
    if(recepient is None):
        notifyInvalidMessage("El usuario seleccionado no existe", serving)
    else:
        prefixLength = 9 + len(recepient.name)
        message = entireString[prefixLength:len(entireString)]
        msg = messageMaker(message, serving.name, MessageEvents.MESSAGE)
        recepient.transport.send(msg)

"""
Function that validates if a room name is unique
Receives the room name to check as a string
Returns true if the room name is unique else returns false
"""
def checkUniqueRoom(roomName):
    try:
        testRoom = rooms[roomName]
        return False
    except KeyError:
        return True

"""
Function that handles the CREATEROOM event
Receives the room name a string and the User object who triggered the event
"""
def createRoom(roomName, serving):
    if checkUniqueRoom(roomName):
        room = Room(roomName, serving)
        room.addUser(serving)
        rooms[roomName] = room
        msg = messageMaker("Se ha creado la habitacion: "+roomName, "[Servidor]", MessageEvents.MESSAGE)
        serving.transport.send(msg)
    else:
        msg = messageMaker("Ya existe una habitacion con ese nombre, usa uno distinto", "[Servidor]", MessageEvents.MESSAGE)
        serving.transport.send(msg)

"""
Function that handles the INVITE event
Receives the room name, the whole string the user sent and the User object who triggered the event
"""
def invite(roomName, entireString, serving):
    try:
        room = rooms[roomName]
        if(serving.name == room.owner.name):
            prefixLength = 8 + len(roomName)
            invitedUsers = entireString[prefixLength:len(entireString)]
            invitedUsers = invitedUsers.split(" ")

            for invited in invitedUsers:
                user = findUser(invited)
                if not (user is None) and user.name != serving.name:
                    if not any(invitation == roomName for invitation in user.pendingInvitations):
                        user.pendingInvitations.append(room.name)
                        print("Invited "+user.name+" to room: "+room.name)
                        msg = messageMaker("Has recibido una invitacion para la habitacion: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                        user.transport.send(msg)
                    else:
                        print(user.name+" has already been invited to the room")

            msg = messageMaker("Se han enviado las invitaciones",  "[Servidor]", MessageEvents.MESSAGE)
            serving.transport.send(msg)
        else:
            notifyInvalidMessage("Solo el dueño de la habitacion puede invitar usuarios", serving)
    except KeyError:
        notifyInvalidMessage("La habitacion "+roomName+" no existe", serving)

"""
Function that handles the JOINROOM event
Receives the room name and the User object who triggered the event
"""
def joinRoom(roomName, serving):
    try:
        room = rooms[roomName]
        if any(pendingInvite == room.name for pendingInvite in serving.pendingInvitations):
            if not any( roomMember.name == serving.name for roomMember in room.connectedUsers):
                room.addUser(serving)
                msg = messageMaker("Te haz unido a la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                serving.pendingInvitations.remove(room.name)
                serving.transport.send(msg)
            else:
                msg = messageMaker("Ya eres parte de la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                serving.pendingInvitations.remove(room.name)
                serving.transport.send(msg)
        else:
            msg = messageMaker("No tienes ninguna invitacion para la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
            serving.transport.send(msg)
    except KeyError:
        notifyInvalidMessage("No existe una sala con el nombre: "+roomName, serving)

"""
Function that handles the ROOMESSAGE event
receives the room name, the whole string the user sent and the User object who triggered the event
"""
def roomMessage(roomName, entireString, serving):
    try:
        room = rooms[roomName]
        if any( insideUser.name == serving.name for insideUser in room.connectedUsers ):
            prefixLength = 12 + len(roomName)
            message = entireString[prefixLength:len(entireString)]
            msg = messageMaker(message, serving.name, MessageEvents.MESSAGE, room.name)
            for user in room.connectedUsers:
                user.transport.send(msg)
        else:
            notifyInvalidMessage("No puedes enviar el mensaje porque no eres parte de la habitacion: "+room.name, serving)
    except KeyError:
        notifyInvalidMessage("La habitacion "+roomName+" no existe", serving)

"""
Function that handles the DISCONNECT event
Receives the user who triggered the event
"""
def disconnectUser(serving):
    serving.transport.close()
    users.remove(serving)
    msg = serving.name+" se ha desconectado"
    message = messageMaker(msg, "[Servidor]", MessageEvents.MESSAGE)
    print(msg)
    sendToAll(message)

"""
Main method for the Server, launches the thread to accept incoming connections
"""
def main(args):
    server.listen()
    print("Servidor corriendo en: "+str(address))
    accept = Thread(target = acceptConnection)
    accept.start()

if __name__ == "__main__":
    main(sys.argv[1:])
