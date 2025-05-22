import socket
import threading
from datetime import datetime

class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()

    def format(self):
        ts = self.timestamp.strftime('%H:%M:%S')
        return f"[{ts}] {self.sender}: {self.content}"

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server closed the connection.")
                break
            print("\n" + data.decode() + "\n> ", end="")
        except:
            print("\nAn error occurred while receiving message.")
            break

# Log in to chat
print("Welcome! Type in your nickname to join chat: ")
username = input()

# Connecting with server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))
client.sendall(username.encode())
print(f"Connected as {username}. You can now start typing your messages.")
print("Type 'exit' to leave the chat.")

# Start receiving thread
receiver_thread = threading.Thread(target=receive_messages, args=(client,), daemon=True)
receiver_thread.start()

# Sending loop
try:
    while True:
        msg = input("> ")
        if msg.strip().lower() == 'exit':
            break
        client.sendall(msg.encode())
except KeyboardInterrupt:
    print("\nDisconnected from chat.")
finally:
    client.close()