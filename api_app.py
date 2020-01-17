import socket

HOST = "localhost"

PORT = 8889

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((HOST, PORT))

print("Welcome dear (this app use the API) !")

print("Submit your requests here, enjoy :) ")

while True:

    msg = input("> ")    

    if(msg != ''):
        
        socket.send(msg.encode())

        response = socket.recv(1024)

        print("> " + response.decode())

    else:
        
        print("tell us what us want !")