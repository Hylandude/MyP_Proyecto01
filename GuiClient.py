from tkinter import *
from tkinter import ttk
import sys
from MessageEvents import MessageEvents
import Client
from threading import Thread

args = sys.argv[1:]

"""
Receives the host and port from command line
Then calls the Client to obtain the transport socket
"""
if len(args) != 2:
    print("Usage: $python3 Client.py <host> <port>");
    sys.exit(1)

port = Client.validatePort(args[1])
transport, message = Client.stablishConnection(args[0], port)


"""
Defines the user interface
"""
window = Tk()

messages = Text(window)
messages.grid(column=0, row=0)
messages.insert(INSERT, message+"\n")

input_user = StringVar()
input_field = Entry(window, text=input_user, width=50)
input_field.grid(column=0, row=1, sticky=E)

chosen_event = StringVar()
combo_box = ttk.Combobox(window, width = 15, textvariable = chosen_event, state="readonly")
combo_box.grid(column=0, row=1, sticky=W)
comboValues = []
for event in MessageEvents:
    comboValues.append(str(event))
combo_box['values'] = comboValues

"""
Function that handles the event when the 'Enter' key is pressed
"""
def Enter_pressed(event):
    try:
        userMessage = input_field.get()
        event = chosen_event.get()
        fullMessage = (event+userMessage).strip()
        messages.insert(INSERT, fullMessage+"\n")
        Client.send(fullMessage, transport)
        input_user.set('')
        return "break"
    except OSError:
        messages.insert(INSERT, "[ANUNCIO]: Has sido desconectado del servidor, reinicia para conectarte de nuevo\n")
        input_user.set('')

frame = Frame(window)
input_field.bind("<Return>", Enter_pressed)
frame.grid(column=0, row=0)

"""
Function that listens to the server
"""
def listenServer(transport):
    listening = True;
    while listening:
        data = Client.getDataFromSocket(transport)
        if(data != ""):
            messages.insert(INSERT, data)
        else:
            listening = False
            transport.close()

listen = Thread(target=listenServer, args=(transport,))
listen.start()
window.mainloop()
