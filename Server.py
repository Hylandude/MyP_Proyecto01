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
                        print ("STATUS EVENT RECEIVED");
                    elif eventReceived == "USERS":
                        print ("USERS EVENT RECEIVED");
                    elif eventReceived == "MESSAGE":
                        print ("MESSAGE EVENT RECEIVED");
                    elif eventReceived == "PUBLICMESSAGE":
                        msg = self.messageMaker(stringReceived, self.serving.name, MessageEvents.MESSAGE)
                        self.sendToAll(msg)
                    elif eventReceived == "CREATEROOM":
                        print ("CREATEROOM EVENT RECEIVED");
                    elif eventReceived == "INVITE":
                        print ("INVITE EVENT RECEIVED");
                    elif eventReceived == "JOINROOM":
                        print ("JOINROOM EVENT RECEIVED");
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

    def notifyInvalidMessage(self, notice):
        msg = self.messageMaker(notice, "[Servidor]", MessageEvents.MESSAGE)
        self.serving.invalidCount += 1
        self.serving.transport.write(msg)

    def identify(self, name):
        if self.serving.name == "":
            print(name+" se ha conectado")
            msg = self.messageMaker("Bienvenido: "+name, "[Servidor]", MessageEvents.MESSAGE)
            self.sendToAll(msg)
            self.serving.setName(name)
        else:
            print(self.serving.name+" trato de identificarse dos veces")
            msg = self.messageMaker("Ya estas identificado, no es posible cambiar tu nombre", "[Servidor]", MessageEvents.MESSAGE)
            self.serving.transport.write(msg)


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
