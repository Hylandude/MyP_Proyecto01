import asyncio
import sys
from MessageEvents import MessageEvents

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 1:
    print("Usage: $python3 server.py <port>");
    sys.exit(1)

class Server(asyncio.Protocol):

    def __init__(self, connections, users):
        print("CALL SERVER CONSTRUCTOR")
        self.connections = connections
        self.users = users
        self.peername = ""
        self.user = None
        self.invalidCount = 0

    def connection_made(self, transport):
        self.connections += [transport]
        self.peername = transport.get_extra_info('sockname')
        self.transport = transport
        print("STABLISHED CONNECTION :"+str(transport))

    def connection_lost(self, exc):
        print("LOST CONNECTION")
        self.connections.remove(self.transport)
        print("\n********\n"+str(exc)+"\n**********\n")
        err = self.peername+" se ha desconectado"
        message = self.messageMaker(err, "[Servidor]", MessageEvents.MESSAGE)
        print(err)
        self.sendToAll(message)

    def data_received(self, data):
        print("DATA RECEIVED")
        if data:
            incomingData = data.decode()
            incomingData = incomingData.split("//")
            eventReceived = str(incomingData[0])
            stringReceived = str(incomingData[1])
            if self.validateEvent(eventReceived):
                if eventReceived == "HANDSHAKE":
                    self.user = stringReceived
                    print(self.user+" se ha conectado")
                    msg = self.messageMaker("Bienvenido: "+self.user, "[Server]", MessageEvents.SERVER)
                    self.sendToAll(msg)
                elif eventReceived == "MESSAGE":
                    print("received: **"+stringReceived+"** From: "+self.user)
                    msg = self.messageMaker(stringReceived, self.user, MessageEvents.MESSAGE)
                    self.sendToAll(msg)
            else:
                msg = self.messageMaker("Mensaje invalido","[Servidor]", MessageEvents.SERVER)
                self.invalidCount += 1
                self.transport.write(msg)
        else:
            msg = self.messageMaker("Mensaje vacio no permitido","[Servidor]", MessageEvents.SERVER)
            self.invalidCount += 1
            self.transport.write(msg)

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
        print("SENDING TO ALL")
        for connection in self.connections:
            print(str(connection))
            connection.write(message)

if __name__ == "__main__":
    connections = []
    users = {}
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: Server(connections, users), "127.0.0.1", args[0])
    server = loop.run_until_complete(coro)

    print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
