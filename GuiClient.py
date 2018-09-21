from tkinter import *
from tkinter import ttk
import sys
from MessageEvents import MessageEvents
import Client
from threading import Thread

args = sys.argv[1:]

if len(args) != 2:
    print("Usage: $python3 Client.py <host> <port>");
    sys.exit(1)

port = Client.validatePort(args[1])
transport, message = Client.stablishConnection(args[0], port)

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

def Enter_pressed(event):
    try:
        userMessage = input_field.get()
        event = chosen_event.get()
        fullMessage = (event+userMessage).strip()
        messages.insert(INSERT, fullMessage+"\n")
        Client.send(fullMessage, transport)
        input_user.set('')
        return "break"
    except BrokenPipeError:
        messages.insert(INSERT, "[ANUNCIO]: Has sido desconectado del servidor, reinicia para conectarte de nuevo\n")
        input_user.set('')

frame = Frame(window)
input_field.bind("<Return>", Enter_pressed)
frame.grid(column=0, row=0)

def listenServer(transport):
    while True:
        data = transport.recv(1024).decode()
        if(data):
            messages.insert(INSERT, data)

listen = Thread(target=listenServer, args=(transport,)).start()
window.mainloop()
