import asyncio
import sys
from sys import stdout
from UserStatus import UserStatus
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

buff = 1024

def data_received(client):
    while True:
        data = client.recv(buff).decode("utf-8")
        validateMessage(data)


def send(data, transport):
    if data:
        transport.send(data.encode("utf-8"))

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

def main(args):
    #Get host and port from command line arguments
    if len(args) != 2:
        print("Usage: $python3 Client.py <host> <port>");
        sys.exit(1)

    try:
        port = int(args[1])
    except ValueError:
        print("PORT must be an integer number");
        sys.exit(1)

    try:
        client = socket(AF_INET, SOCK_STREAM)
        client.connect((args[0],port))
        print("Conectado en: "+str((args[0],port)))
    except ConnectionRefusedError:
        print("No fue posible conectarse")
        sys.exit(1)

    listenServer = Thread(target=data_received, args=(client,))
    readInput = Thread(target=consoleInput, args=(client,))
    listenServer.start()
    readInput.start()

if __name__ == "__main__":
    main(sys.argv[1:])
