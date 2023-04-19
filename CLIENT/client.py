import socket
import json
import time
from os import system

# Ask for IP, port, and username
ip = input("Enter IP: ")
port = int(input("Enter port: "))
username = input("Enter username: ")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = (ip, port)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

# Receive the data in small chunks and retransmit it
while True:
    try:
        message = input(f'{username}, введите сообщение ')
        text_message = f'{username}> - {message}' 
        sock.send(bytes(f'{text_message}\n'.encode()))
        # Store the data in a json file

        data = sock.recv(1024)
        if data:
            print(data.decode())
    except Exception as e:
        print(e)

# Clean up the connection
print('closing socket')
system('cls')
sock.close()