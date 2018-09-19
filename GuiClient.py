from tkinter import *
from tkinter import ttk
import sys

import Client

window = Tk()

messages = Text(window)
messages.grid(column=0, row=0)

input_user = StringVar()
input_field = Entry(window, text=input_user, width=50)
input_field.grid(column=0, row=1, sticky=E)

chosen_event = StringVar()
combo_box = ttk.Combobox(window, width = 15, textvariable = chosen_event, state="readonly")
combo_box.grid(column=0, row=1, sticky=W)
combo_box['values'] = ["text 1", "text 2", "text3"]

def Enter_pressed(event):
    userMessage = input_field.get()
    event = chosen_event.get()
    fullMessage = event+" "+userMessage
    messages.insert(INSERT, '%s\n' % fullMessage)
    input_user.set('')
    return "break"

frame = Frame(window)
input_field.bind("<Return>", Enter_pressed)
frame.grid(column=0, row=0)

window.mainloop()
