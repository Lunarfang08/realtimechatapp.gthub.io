import socket
import threading

# Function to handle client connections
def client_thread(conn, addr):
    try:
        # Receiving the nickname from the client
        nickname = conn.recv(1024).decode()
        print(f"{nickname} has joined the chat from {addr}.")
        # Broadcasting the joining message to other clients
        broadcast(f"{nickname} has joined the chat!".encode())

        while True:
            # Receiving messages from client
            message = conn.recv(1024).decode()
            if message == "/quit":  # Client sends '/quit' to disconnect
                remove(conn)
                break
            elif message:
                # Broadcasting messages to other clients
                print(f"{nickname}: {message}")
                broadcast(f"{nickname}: {message}".encode())
            else:
                # Handling client disconnection
                remove(conn)
                break
    except:
        # Handling any exception by removing the client
        remove(conn)
    finally:
        # Closing the connection
        conn.close()

# Function to broadcast messages to all clients except the sender
def broadcast(message, connection=None):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                # Removing the client on failed message sending
                remove(client)

# Function to remove a client from the list
def remove(connection):
    if connection in clients:
        clients.remove(connection)
        print(f"Client {connection.getpeername()} disconnected")

# Creating a socket object for the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Server IP and Port setup
IP_address = '127.0.0.1'
Port = 12345
server.bind((IP_address, Port))
server.listen(100)  # Server can accept up to 100 connections

clients = []  # List to keep track of connected clients

# Accepting multiple client connections
while True:
    conn, addr = server.accept()
    clients.append(conn)
    print(f"Connection established with {addr}")
    # Starting a new thread for each client connection
    threading.Thread(target=client_thread, args=(conn, addr)).start()
