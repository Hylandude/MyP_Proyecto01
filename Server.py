import asyncio
import sys
from MessageEvents import MessageEvents

clients = {}

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 1:
    print("Usage: $python3 server.py <port>");
    sys.exit(1)

def validateEvent(eventType):
    try:
        event = str(MessageEvents[eventType])
        eventType = eventType+"//"
        print ("Validating: "+eventType+"---"+event)
        return eventType == event
    except KeyError:
        return False

def sendToAll(clients, data):
    print(clients)
    for client, writer in clients.items():
        print("Sending: "+data.decode()+" to: "+client);
        writer.write(data)
        writer.drain()

#reads data from the input socket and sends it back
async def server_main(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()

        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))
        clients[addr[0]+str(addr[1])] = writer
        eventType = message.split("//")[0]
        if validateEvent(eventType):
            sendToAll(clients, data)
        else:
            print("invalid event")
            writer.write("Mensaje invalido".encode())
            await writer.drain()

        if eventType == "CLOSE":
            print("Close the client socket")
            writer.close()

#start server
try:
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(server_main, "127.0.0.1", args[0], loop=loop)
    server = loop.run_until_complete(coro)
except Exception as ex:
    print("No se pudo iniciar el servidor, verifica que el puerto sea un numero entero")
    sys.exit(1)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
