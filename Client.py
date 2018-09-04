import asyncio
import sys
from sys import stdout

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 2:
    print("Usage: $python3 client.py <host> <port>");
    sys.exit(1)

class Client(asyncio.Protocol):
    def __init__(self, loop, **kwargs):
        self.is_open = False
        self.loop = loop

    def connection_made(self, transport):
        print("CONNECTION MADE")
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.is_open = True

    def connection_lost(self, exc):
         self.is_open = False
         self.loop.stop()

    def data_received(self, data):
        print("DATA Received")
        while not hasattr(self, "output"): #Wait until output is established
            pass
        if data:
            message = data.decode()
            print("MESSAGE: "+message+"---")
            self.output(message+"\n")

    def send(self, data):
        if data:
            self.transport.write(data.encode())

    def initializeOutput(self, loop):
        self.output = self.stdoutput
        self.output("Connected to {0}:{1}\n".format(*self.sockname))
        while True:
            msg = input("Escribe tu mensaje\n")
            self.send(msg)

    def stdoutput(self, data):
        stdout.write(data.strip() + '\n')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    userClient = Client(loop)
    coro = loop.create_connection(lambda: userClient, args[0], args[1])
    server = loop.run_until_complete(coro)
    asyncio.async(userClient.initializeOutput(loop))
    loop.run_forever()
    loop.close()



loop.close()
