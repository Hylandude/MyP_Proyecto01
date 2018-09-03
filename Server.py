import asyncio
import sys

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 1:
    print("Usage: $python3 server.py <port>");
    sys.exit(1)

#reads data from the input socket and sends it back
async def server_main(reader, writer):
    clients = []
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print("Received %r from %r" % (message, addr))

        close_sequence = message.split("_")[0]

        print("Send: %r" % message)
        writer.write(data)
        await writer.drain()

        if close_sequence == "close":
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
