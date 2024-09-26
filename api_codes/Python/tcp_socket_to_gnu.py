import socket
import time

# Define the server address and port
server_address = ('<SERVER_IP>', 1234)  # Replace <SERVER_IP> with the server's actual IP address

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

try:
    while True:
        message = "Hello, World!"
        client_socket.sendall(message.encode())
        print('Sent:', message)
        time.sleep(1)  # Send every 1 second

finally:
    client_socket.close()
