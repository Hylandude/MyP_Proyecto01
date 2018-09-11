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
    print("Usage: $python3 server.py <port>");
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
        print("LOST CONNECTION")
        self.connections.remove(self.transport)
        print("\n********\n"+str(exc)+"\n**********\n")
        err = self.peername+" se ha desconectado"
        message = self.messageMaker(err, "[Servidor]", MessageEvents.MESSAGE)
        print(err)
        self.sendToAll(message)

    def data_received(self, data):
        if data:
            incomingData = data.decode()
            print("received: "+incomingData+" \nFrom: "+self.serving.name)
            incomingData = incomingData.split("//")
            eventReceived = str(incomingData[0])
            stringReceived = str(incomingData[1])
            if self.validateEvent(eventReceived):
                if eventReceived == "IDENTIFY":
                    self.serving.setName(stringReceived)
                    print(self.serving.name+" se ha conectado")
                    msg = self.messageMaker("Bienvenido: "+self.serving.name, "[Server]", MessageEvents.MESSAGE)
                    self.sendToAll(msg)
                elif eventReceived == "MESSAGE":
                    if self.serving.name != "":
                        msg = self.messageMaker(stringReceived, self.serving.name, MessageEvents.MESSAGE)
                        self.sendToAll(msg)
                    else:
                        msg = self.messageMaker("No puedes enviar mensajes hasta que te autentiques", "[Servidor]", MessageEvents.MESSAGE)
                        self.serving.invalidCount += 1
                        self.serving.transport.write(msg)
            else:
                msg = self.messageMaker("Mensaje invalido","[Servidor]", MessageEvents.MESSAGE)
                self.serving.invalidCount += 1
                self.serving.transport.write(msg)
        else:
            msg = self.messageMaker("Mensaje vacio no permitido","[Servidor]", MessageEvents.MESSAGE)
            self.serving.invalidCount += 1
            self.serving.transport.write(msg)

    def messageMaker(self, message, author, event):
        return (str(event)+author+": "+message).encode()

    def validateEvent(self, eventType):
        try:
            event = str(MessageEvents[eventType])
            eventType = eventType+"//"
            return eventType == event
        except KeyError:
            return False

    def sendToAll(self, message):
        for user in self.users:
            user.transport.write(message)

if __name__ == "__main__":
    users = []
    rooms = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: Server(rooms, users), "127.0.0.1", args[0])
    server = loop.run_until_complete(coro)

    print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
