import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

class ChatClient:
    def __init__(self):
        # TCP connection via Internet
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.window = tk.Tk()
        self.window.title("Chat Client")

        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, state='disabled', height=20)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Send message when typed in and hit enter
        self.entry_field = tk.Entry(self.window)
        self.entry_field.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry_field.bind("<Return>", self.send_message)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Asking for username to log in to chat
        self.username = self.ask_username()
        if not self.username:
            self.window.destroy()
            return
        try:
            self.client.connect(('127.0.0.1', 9999))
            self.client.sendall(self.username.encode())
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect to server: {e}")
            self.window.destroy()
            return

        # Message for the client
        self.append_chat(f"Connected as {self.username}. Type your message and press Enter.")

        # Setting up receiving thread, when other tasks finish it can also be ended
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()

    # Window for entering username
    def ask_username(self):
        return simpledialog.askstring("Username", "Enter your nickname:", parent=self.window)

    # Function for receive_message thread
    def receive_messages(self):
        while True:
            try:
                data = self.client.recv(1024)
                if not data:
                    self.append_chat("Server closed the connection.")
                    break
                self.append_chat(data.decode())
            except Exception as e:
                self.append_chat("Error receiving message.")
                break

    def send_message(self, event=None):
        msg = self.entry_field.get().strip()
        if msg.lower() == "exit":
            self.on_close()
            return
        if msg:
            try:
                self.client.sendall(msg.encode())
                self.entry_field.delete(0, tk.END)
            except Exception as e:
                self.append_chat(f"Error sending message: {e}")
                self.client.close()

    # Method to add to chat
    def append_chat(self, msg):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, msg + '\n')
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def on_close(self):
        self.client.close()
        self.window.destroy()

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ChatClient()
    app.run()
