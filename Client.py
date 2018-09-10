import asyncio
import sys
from sys import stdout

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
        print("CONNECTION MADE")
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.is_open = True
        self.transport.write(("HANDSHAKE//"+self.username).encode())

    def connection_lost(self, exception):
        print("CONNECTION LOST")
        print(exception)
        self.is_open = False
        self.loop.stop()

    def data_received(self, data):
        print("DATA Received")
        while not hasattr(self, "output"):
            pass
        if data:
            message = data.decode()
            print("MESSAGE: "+message+"---")

    def send(self, data):
        if data:
            message = "MESSAGE//"+data
            self.transport.write(message.encode())

    def initializeOutput(self, loop):
        print("Connected to {0}:{1}\n".format(*self.sockname))
        while True:
            msg = input("Escribe tu mensaje\n")
            self.send(msg)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    userClient = Client(loop, args[2])
    coro = loop.create_connection(lambda: userClient, args[0], args[1])
    server = loop.run_until_complete(coro)
    asyncio.async(userClient.initializeOutput(loop))
    loop.run_forever()
    loop.close()



loop.close()
