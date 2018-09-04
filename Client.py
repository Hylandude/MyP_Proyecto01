import asyncio
import sys

#Get host and port from command line arguments
args = sys.argv
args = args[1:len(args)]
if len(args) != 2:
    print("Usage: $python3 client.py <host> <port>");
    sys.exit(1)

#reads a message from command line, sends it to server and prints response
async def tcp_echo_client(loop):
    try:
        reader, writer = await asyncio.open_connection(args[0], args[1], loop=loop)
    except ConnectionRefusedError:
        print("Error conectado al servidor, verifica la direccion y puerto")
        sys.exit(1)

    close_sequence = "open"
    while close_sequence != "close":
        message = input("Escribe tu mensaje:\n")
        writer.write(message.encode())

        data = await reader.read(100)
        print('Received: %r' % data.decode())
        close_sequence = data.decode().split("_")[0]
        print("close_sequence: "+close_sequence)

    print('Close the socket')
    writer.close()

#initializes async loop for client
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(loop))
loop.close()
