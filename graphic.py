import tkinter as tk
from Chatbot import ChatterBot
from tkinter import *

window = tk.Tk()
window.title("chatter bot")
window.geometry("250x500")

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)

scroll_list = Listbox(window, yscrollcommand=scrollbar.set, width=250, justify='right',
                      bg='#ffbdde')

chatterBot = ChatterBot(tk, scroll_list)
scroll_list.pack(side=RIGHT, fill=BOTH)
scrollbar.config(command=scroll_list.yview)


# Create an event handler
def handle_keypress(event):
    chatterBot.start_chat()


window.bind("<Return>", handle_keypress)
window.mainloop()
