#!/usr/bin/env python3

import asyncio
import sys
from sys import stdout
from UserStatus import UserStatus
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

buff = 1024

"""
Function that handles the data received from the server decodes the data and prints on console
Receives the socket to read from
"""
def data_received(transport):
    while True:
        data = transport.recv(buff).decode()
        print(data)

"""
Function that reads data from sockets and returns it as a string
Receives the sicket to read from
"""
def getDataFromSocket(transport):
    data = transport.recv(buff).decode()
    return data

"""
Function that sends data to the server
Receives the data as a string and the socket to send from
"""
def send(data, transport):
    if data:
        data = (data+"\r\n").encode()
        transport.send(data)

"""
Function that reads the input from the console and sends the message
"""
def consoleInput(transport):
    while True:
        msg = input()
        send(msg, transport)

"""
Deprecated
"""
# def validateMessage(message):
#     try:
#         incomingData = message.split(" ")
#         eventReceived = incomingData[0]
#         stringReceived = message[len(eventReceived)+1:]
#         if eventReceived == "PUBLICMESSAGE" or eventReceived == "MESSAGE":
#             print(stringReceived)
#     except KeyError:
#         print("Se ha recivido un mensaje invalido")

"""
Function that connects the client socket to the server
Receives the host and port both as strings
Returns the connected socket and a message indicating the status as a tuple
"""
def stablishConnection(host, port):
    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((host,port))
        successMessage = "Conectado en: "+str((host,port))
        print(successMessage)
        return (transport, successMessage)
    except ConnectionRefusedError:
        print("No fue posible conectarse")
        sys.exit(1)

"""
Function that validates if the received port is an integer
Returns the port number as an interger or exits y false
"""
def validatePort(portString):
    try:
        port = int(portString)
        return port
    except ValueError:
        print("PORT must be an integer number");
        sys.exit(1)

"""
Main method for the client, launches the console input interface
"""
def main(args):
    #Get host and port from command line arguments
    if len(args) != 2:
        print("Usage: $python3 Client.py <host> <port>");
        sys.exit(1)

    port = validatePort(args[1])

    transport, message = stablishConnection(args[0], port)

    try:
        listenServer = Thread(target=data_received, args=(transport,))
        readInput = Thread(target=consoleInput, args=(transport,))
        listenServer.start()
        readInput.start()
    except KeyboardInterrupt:
        listenServer.join()
        readInput.join()

if __name__ == "__main__":
    main(sys.argv[1:])
