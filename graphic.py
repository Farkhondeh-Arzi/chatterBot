import tkinter as tk
from Chatbot import ChatterBot


window = tk.Tk()
window.title("chatter bot")
window.geometry("700x350")

chatterBot = ChatterBot(tk)


# Create an event handler
def handle_keypress(event):
    chatterBot.start_chat()


window.bind("<Return>", handle_keypress)
window.mainloop()