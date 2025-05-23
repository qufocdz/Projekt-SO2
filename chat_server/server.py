import threading
import socket
from datetime import datetime

# Mutexes used in synchronization
broadcast_mutex = threading.Lock()
connection_mutex = threading.Lock()

# Shared resources
open_connections = []

# Class describing message format
class Message:
    def __init__(self, sender, content):
        self.sender = sender
        self.content = content
        self.timestamp = datetime.now()

    def format(self):
        ts = self.timestamp.strftime('%H:%M:%S')
        return f"[{ts}] {self.sender}: {self.content}"

# Class extending Thread for each Client's Connection
class ClientConnection(threading.Thread):
    def __init__(self, client, address, username):
        super().__init__()
        self.client = client
        self.address = address
        self.username = username
        self.running = True

    # Method assigned to Thread by overriding
    def run(self):
        print(f"[{self.username}] connected from {self.address}")
        try:
            while self.running:
                data = self.client.recv(1024)
                if not data:
                    break
                message_text = data.decode().strip()
                message = Message(self.username, message_text)

                # Acquire broadcast and connection locks, entering critical section
                broadcast_mutex.acquire()
                connection_mutex.acquire()

                # Copying current connections list, freeing up resource
                connections_copy = list(open_connections)
                connection_mutex.release()

                # Broadcasting Client's message to everyone, broadcasting critical section
                for conn in connections_copy:
                    try:
                        conn.client.sendall(message.format().encode())
                    except Exception as e:
                        print(f"Failed to send to {conn.username}: {e}")

                # Releasing broadcasting
                broadcast_mutex.release()
        except Exception as e:
            print(f"Error with {self.username}: {e}")
        finally:
            print(f"[{self.username}] disconnected.")
            self.stop()

    # Stop method for clean-up and disconnecting safely
    def stop(self):
        self.running = False
        self.client.close()
        # Acquiring connection mutex in order to remove Client
        connection_mutex.acquire()
        try:
            if self in open_connections:
                open_connections.remove(self)
        finally:
            connection_mutex.release()

# Setting up server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5) # Max number of chat users
print("Server set up on port 9999. Currently listening.")

# Main server program
while True:
    client, addr = server.accept()
    print(f"Connection attempt from {addr}")

    # Trying to log user into chat
    try:
        username = client.recv(1024).decode().strip()
        if not username:
            client.close()
            continue
    except Exception as e:
        print(f"Failed to receive username from {addr}: {e}")
        client.close()
        continue

    # Acquiring connection mutex in order to add Client to chat
    connection_mutex.acquire()
    if not any(conn.address == addr for conn in open_connections):
        new_connection = ClientConnection(client, addr, username)
        open_connections.append(new_connection)
        new_connection.start()
        print(f"Connection established with {username} at {addr}")
    else:
        client.sendall("Duplicate connection.".encode())
        client.close()
    # Releasing connection mutex, exiting connection critical section
    connection_mutex.release()
