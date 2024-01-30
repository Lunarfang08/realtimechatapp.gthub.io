import socket
import threading

# Function to handle receiving messages from the server
def receive_message(client_socket):
    while True:
        try:
            # Receiving and printing messages from the server
            message = client_socket.recv(1024).decode()
            if message:
                print(message)
        except:
            # Handling disconnection from the server
            print("Disconnected from the server.")
            client_socket.close()
            break

# Creating a socket object for the client
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server IP and Port setup for the client
IP_address = '127.0.0.1'
Port = 12345
server.connect((IP_address, Port))

# Sending the client's nickname to the server
nickname = input("Enter your nickname: ")
server.send(nickname.encode())

# Starting a thread to receive messages from the server
threading.Thread(target=receive_message, args=(server,)).start()

# Handling sending messages to the server
while True:
    message = input('')
    if message == "/quit":
        # Sending '/quit' command to the server to disconnect
        server.send(message.encode())
        server.close()
        break
    else:
        # Sending regular messages to the server
        server.send(message.encode())
