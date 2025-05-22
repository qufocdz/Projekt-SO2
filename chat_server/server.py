import threading
import socket
from datetime import datetime

class ClientConnection(threading.Thread):
    def __init__(self, client, address, username):
        super().__init__()
        self.client = client
        self.address = address
        self.username = username
        self.running = True

    def run(self):
        print(f"[{self.username}] connected from {self.address}")
        try:
            while self.running:
                data = self.client.recv(1024)
                if not data:
                    break
                message_text = data.decode().strip()
                message = Message(self.username, message_text)
                print(message.format())
                # Echo back to client (or broadcast later)
                self.client.sendall(f"Server received: {message.format()}".encode())
        except Exception as e:
            print(f"Error with {self.username}: {e}")
        finally:
            print(f"[{self.username}] disconnected.")
            self.client.close()

    def stop(self):
        self.running = False
        self.client.close()

class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()

    def format(self):
        ts = self.timestamp.strftime('%H:%M:%S')
        return f"[{ts}] {self.sender}: {self.content}"

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)

clients_addresses = []
open_connections = []

print("Server is listening on port 9999...")

while True:
    client, addr = server.accept()
    print(f"Connection attempt from {addr}")

    try:
        username = client.recv(1024).decode().strip()
        if not username:
            client.close()
            continue
    except Exception as e:
        print(f"Failed to receive username from {addr}: {e}")
        client.close()
        continue

    if addr not in clients_addresses:
        clients_addresses.append(addr)
        new_connection = ClientConnection(client, addr, username)
        new_connection.start()
        open_connections.append(new_connection)
        print(f"Connection established with {username} at {addr}")