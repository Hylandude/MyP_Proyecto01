import asyncio
import sys
from sys import stdout
from UserStatus import UserStatus

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 3:
    print("Usage: $python3 client.py <host> <port> <username>");
    sys.exit(1)

class Client(asyncio.Protocol):

    def __init__(self, loop, username):
        self.username = username
        self.is_open = False
        self.loop = loop

    def connection_made(self, transport):
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.is_open = True
        #self.transport.write(("HANDSHAKE//"+self.username).encode())

    def connection_lost(self, exception):
        print("CONNECTION LOST")
        print(str(exception))
        self.is_open = False
        self.loop.stop()

    def data_received(self, data):
        while not hasattr(self, "output"):
            pass
        if data:
            message = data.decode()
            self.validateMessage(message)

    def send(self, data):
        if data:
            #message = "MESSAGE//"+data
            message = data
            self.transport.write(message.encode())

    async def initializeOutput(self, loop):
        self.output = self.stdoutput
        self.output("Te has conectado a: "+str(self.sockname))
        while True:
            msg = await loop.run_in_executor(None, input)
            self.send(msg)

    def validateMessage(self, message):
        try:
            incomingData = message.split("//")
            eventReceived = str(incomingData[0])
            stringReceived = str(incomingData[1])
            if eventReceived == "MESSAGE":
                self.output(stringReceived)
        except KeyError:
            self.output("Se ha recivido un mensaje invalido")

    def stdoutput(self, data):
        stdout.write(data+ '\n')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    userClient = Client(loop, args[2])
    coro = loop.create_connection(lambda: userClient, args[0], args[1])
    server = loop.run_until_complete(coro)
    asyncio.async(userClient.initializeOutput(loop))
    loop.run_forever()
    loop.close()
