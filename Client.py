import asyncio
import sys
from sys import stdout
from UserStatus import UserStatus
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

buff = 1024

def data_received(transport):
    while True:
        data = transport.recv(buff).decode()
        print(data)
        #validateMessage(data)


def send(data, transport):
    if data:
        print(data)
        data = (data+"\r\n").encode()
        print(data)
        transport.send(data)

def consoleInput(transport):
    while True:
        msg = input()
        send(msg, transport)

def validateMessage(message):
    try:
        incomingData = message.split(" ")
        eventReceived = incomingData[0]
        stringReceived = message[len(eventReceived)+1:]
        if eventReceived == "PUBLICMESSAGE" or eventReceived == "MESSAGE":
            print(stringReceived)
    except KeyError:
        print("Se ha recivido un mensaje invalido")

def stablishConnection(host, port):
    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((host,port))
        successMessage = "Conectado en: "+str((host,port))
        print(successMessage)
        return (client, successMessage)
    except ConnectionRefusedError:
        print("No fue posible conectarse")
        sys.exit(1)

def validatePort(portString):
    try:
        port = int(portString)
        return port
    except ValueError:
        print("PORT must be an integer number");
        sys.exit(1)

def main(args):
    #Get host and port from command line arguments
    if len(args) != 2:
        print("Usage: $python3 Client.py <host> <port>");
        sys.exit(1)

    port = validatePort(args[1])

    transport, message = stablishConnection(args[0], port)

    try:
        listenServer = Thread(target=data_received, args=(transport,))
        readInput = Thread(target=consoleInput, args=(client,))
        listenServer.start()
        readInput.start()
    except KeyboardInterrupt:
        listenServer.join()
        readInput.join()

if __name__ == "__main__":
    main(sys.argv[1:])
