import asyncio
import sys
from MessageEvents import MessageEvents
from UserStatus import UserStatus
from User import User
from Room import Room

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 1:
    print("Usage: $python3 Server.py <port>");
    sys.exit(1)

class Server(asyncio.Protocol):

    def __init__(self, rooms, users):
        self.rooms = rooms
        self.users = users
        self.serving = None

    def connection_made(self, transport):
        print(transport)
        print(type(transport))
        newUser = User(transport)
        self.users += [newUser]
        self.serving = newUser
        print("STABLISHED CONNECTION :"+str(transport.get_extra_info('sockname')))

    def connection_lost(self, exc):
        self.users.remove(self.serving)
        msg = self.serving.name+" se ha desconectado"
        message = self.messageMaker(msg, "[Servidor]", MessageEvents.MESSAGE)
        print(msg)
        self.sendToAll(message)

    def data_received(self, data):
        if data:
            incomingString = data.decode()
            incomingData = incomingString.split(" ")
            print("received: "+incomingString+" \nFrom: "+self.serving.name)
            eventReceived = incomingData[0]
            if self.validateEvent(eventReceived):
                if eventReceived == "IDENTIFY":
                    if len(incomingData) != 2:
                        print ("Invalid IDENTIFY event")
                        self.notifyInvalidMessage(MessageEvents.validList())
                    else:
                        self.identify(incomingData[1])
                elif self.serving.name != "":
                    if eventReceived == "STATUS":
                        if len(incomingData) != 2:
                            print("Invalid STATUS event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.status(incomingData[1])
                    elif eventReceived == "USERS":
                        if len(incomingData) != 1:
                            print("Invalid USERS event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.sendUserList()
                    elif eventReceived == "MESSAGE":
                        if len(incomingData) < 3:
                            print("Invalid MESSAGE event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.personalMessage(incomingData[1], incomingString)
                    elif eventReceived == "PUBLICMESSAGE":
                        if len(incomingData) < 2:
                            print("Invalid PUBLICMESSAGE event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            message = incomingString[14:len(incomingString)]
                            msg = self.messageMaker(message, self.serving.name, MessageEvents.PUBLICMESSAGE)
                            self.sendToAll(msg)
                    elif eventReceived == "CREATEROOM":
                        print ("CREATEROOM EVENT RECEIVED");
                        if len(incomingData) != 2:
                            print("Invalid USERS event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.createRoom(incomingData[1])
                    elif eventReceived == "INVITE":
                        if len(incomingData) < 3:
                            print("Invalid INVITE event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.invite(incomingData[1], incomingString)
                    elif eventReceived == "JOINROOM":
                        if len(incomingData) != 2:
                            print("Invalid JOINROOM event")
                            self.notifyInvalidMessage(MessageEvents.validList())
                        else:
                            self.joinRoom(incomingData[1])
                    elif eventReceived == "ROOMESSAGE":
                        print ("ROOMESSAGE EVENT RECEIVED");
                    elif eventReceived == "DISCONNECT":
                        print ("DISCONNECT EVENT RECEIVED");
                else:
                    print("Usuario no autenticado intento un evento")
                    self.notifyInvalidMessage("No puedes enviar mensajes hasta que te autentiques")

            else:
                print("Se recibio un mensaje invalido")
                self.notifyInvalidMessage(MessageEvents.validList())

        else:
            print("Se recibio un mensaje vacio")
            self.notifyInvalidMessage("Mensaje vacio no permitido")

    def messageMaker(self, message, author, event):
        return (str(event)+author+": "+message).encode()

    def validateEvent(self, eventType):
        try:
            return eventType+" " == str(MessageEvents[eventType])
        except KeyError:
            return False

    def sendToAll(self, message):
        for user in self.users:
            user.transport.write(message)

    def findUser(self, searchedName):
        recepient = None
        for user in users:
            if(user.name == searchedName):
                recepient = user
        return recepient

    def notifyInvalidMessage(self, notice):
        msg = self.messageMaker(notice, "[Servidor]", MessageEvents.MESSAGE)
        self.serving.invalidCount += 1
        self.serving.transport.write(msg)

    def identify(self, name):
        if self.serving.name == "":
            sameNameUser = self.findUser(name)
            if sameNameUser is None:
                print(name+" se ha conectado")
                msg = self.messageMaker("Bienvenido: "+name, "[Servidor]", MessageEvents.PUBLICMESSAGE)
                self.sendToAll(msg)
                self.serving.setName(name)
            else:
                print("Se recibio un nombre duplicado")
                msg = self.messageMaker("El nombre que escogiste ya esta en uso", "[Servidor]", MessageEvents.MESSAGE)
                self.serving.transport.write(msg)
        else:
            print(self.serving.name+" trato de identificarse dos veces")
            msg = self.messageMaker("Ya estas identificado, no es posible cambiar tu nombre", "[Servidor]", MessageEvents.MESSAGE)
            self.serving.transport.write(msg)

    def status(self, statusSelected):
        try:
            self.serving.setStatus(UserStatus[statusSelected.upper()])
        except KeyError:
            print("Received invalid status on event")
            self.notifyInvalidMessage("Status invalido. Debe ser 'ACTIVE', 'AWAY' o 'BUSY'")

    def sendUserList(self):
        userString = ""
        for user in self.users:
            if user.isAuthenticated:
                userString += user.name+", "
        userString = userString[0:len(userString)-2]
        msg = self.messageMaker(userString, "[Servidor]", MessageEvents.MESSAGE)
        self.serving.transport.write(msg)

    def personalMessage(self, recepientName, entireString):
        recepient = self.findUser(recepientName)
        if(recepient is None):
            self.notifyInvalidMessage("El usuario seleccionado no existe")
        else:
            prefixLength = 9 + len(recepient.name)
            message = entireString[prefixLength:len(entireString)]
            msg = self.messageMaker(message, self.serving.name, MessageEvents.MESSAGE)
            recepient.transport.write(msg)

    def checkUniqueRoom(self, roomName):
        try:
            testRoom = self.rooms[roomName]
            return False
        except KeyError:
            return True

    def createRoom(self, roomName):
        if self.checkUniqueRoom(roomName):
            room = Room(roomName, self.serving)
            room.addUser(self.serving)
            self.rooms[roomName] = room
            msg = self.messageMaker("Se ha creado la habitacion: "+roomName, "[Servidor]", MessageEvents.MESSAGE)
            self.serving.transport.write(msg)
        else:
            msg = self.messageMaker("Ya existe una habitacion con ese nombre, usa uno distinto", "[Servidor]", MessageEvents.MESSAGE)
            self.serving.transport.write(msg)

    def invite(self, roomName, entireString):
        try:
            room = self.rooms[roomName]
            if(self.serving.name == room.owner.name):
                prefixLength = 8 + len(roomName)
                invitedUsers = entireString[prefixLength:len(entireString)]
                invitedUsers = invitedUsers.split(" ")

                for invited in invitedUsers:
                    user = self.findUser(invited)
                    if not (user is None) and user.name != self.serving.name:
                        if not any(invitation == roomName for invitation in user.pendingInvitations):
                            user.pendingInvitations.append(room.name)
                            print("Invited "+user.name+" to room: "+room.name)
                            msg = self.messageMaker("Has recibido una invitacion para la habitacion: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                            user.transport.write(msg)
                        else:
                            print(user.name+" has already been invited to the room")

                msg = self.messageMaker("Se han enviado las invitaciones",  "[Servidor]", MessageEvents.MESSAGE)
                self.serving.transport.write(msg)
            else:
                self.notifyInvalidMessage("Solo el dueño de la habitacion puede invitar usuarios")
        except KeyError:
            self.notifyInvalidMessage("La habitacion "+roomName+" no existe")

    def joinRoom(self, roomName):
        try:
            room = self.rooms[roomName]
            if any(pendingInvite == room.name for pendingInvite in self.serving.pendingInvitations):
                if not any( roomMember.name == self.serving.name for roomMember in room.connectedUsers):
                    room.addUser(self.serving)
                    msg = self.messageMaker("Te haz unido a la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                    self.serving.pendingInvitations.remove(room.name)
                    self.serving.transport.write(msg)
                else:
                    msg = self.messageMaker("Ya eres parte de la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                    self.serving.pendingInvitations.remove(room.name)
                    self.serving.transport.write(msg)
            else:
                msg = self.messageMaker("No tienes ninguna invitacion para la sala: "+room.name, "[Servidor]", MessageEvents.MESSAGE)
                self.serving.transport.write(msg)
        except KeyError:
            self.notifyInvalidMessage("No existe una sala con el nombre: "+roomName)

if __name__ == "__main__":
    users = []
    rooms = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: Server(rooms, users), "127.0.0.1", args[0])
    server = loop.run_until_complete(coro)

    print("Servidor corriendo en: "+str(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
