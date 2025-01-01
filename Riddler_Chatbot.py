import json
from difflib import get_close_matches
from tkinter import Tk, Entry, Button, Text, Scrollbar, Frame

class Chatbot:
    def __init__(self, window):
        self.window = window
        self.fullscreen = False
        window.title('Riddler Assistant')
        window.geometry('800x600')  # Set a default size
        window.resizable(True, True)  # Allow resizing

        # Create main frame
        main_frame = Frame(window)
        main_frame.pack(fill='both', expand=True)

        # Create message session
        self.message_session = Text(main_frame, bd=3, relief="flat", font=("Arial", 12), undo=True, wrap="word")
        self.message_session.config(bg="whitesmoke", fg="black", state='disabled')
        self.message_session.pack(side='left', fill='both', expand=True, padx=10, pady=10)

        # Create scrollbar
        self.overscroll = Scrollbar(main_frame, command=self.message_session.yview)
        self.overscroll.pack(side='right', fill='y', padx=10, pady=10)
        self.message_session["yscrollcommand"] = self.overscroll.set

        # Create bottom frame
        bottom_frame = Frame(window)
        bottom_frame.pack(fill='x', padx=10, pady=10)

        # Create message entry
        self.Message_Entry = Entry(bottom_frame, font=('Arial', 12))
        self.Message_Entry.pack(side='left', fill='x', expand=True, padx=10)
        self.Message_Entry.bind('<Return>', self.reply_to_you)

        # Create send button
        self.send_button = Button(bottom_frame, text='Send', fg='white', bg="dodgerblue", font=('Arial', 12), command=self.reply_to_you)
        self.send_button.pack(side='left', padx=10)

        self.Brain = json.load(open('knowledge.json'))

        window.bind('<F11>', self.toggle_fullscreen)  # Bind F11 key to toggle fullscreen
        window.bind('<Escape>', self.exit_fullscreen)  # Bind Escape key to exit fullscreen

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.window.attributes("-fullscreen", self.fullscreen)
    
    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.window.attributes("-fullscreen", False)

    def add_chat(self, message):
        self.Message_Entry.delete(0, 'end')
        self.message_session.config(state='normal')
        self.message_session.insert('end', message)
        self.message_session.see('end')
        self.message_session.config(state='disabled')

    def reply_to_you(self, event=None):
        message = self.Message_Entry.get().lower()
        user_message = 'you: ' + message + '\n'
        close_match = get_close_matches(message, self.Brain.keys())
        if close_match:
            reply = 'Riddler: ' + self.Brain[close_match[0]][0] + '\n'
        else:
            reply = 'Riddler: ' + "Can't find it in my knowledge base\n"
        self.add_chat(user_message)
        self.add_chat(reply)


root = Tk()
Chatbot(root)
root.mainloop()


