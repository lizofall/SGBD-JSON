import socket

HOST = "localhost"

PORT = 8888

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect((HOST, PORT))

print("\nWelcome to our Database Managing App !")

print("\nPlease, proceed first to authentication")

authenticated = 'false'

#Credentials requirer

def ask_for_credentials():

    login = input('\nLogin: ')

    password = input('\nPassword: ')

    return "Credentials "+ login + " " + password + " ;"

while True:

    while authenticated == 'false':

        print('\n--- Authentication ---')

        msg = ask_for_credentials()

        socket.send(msg.encode())

        response = socket.recv(1024)

        authenticated = response.decode()

        if(authenticated == 'true'):

            print('\n--------------------------------------------------------')

            print('\n Happy to see you again \n')

            print("Submit your requests here, enjoy :) \n ")

        else:

            print('\nAuthenticated failed, please verify your credentials')

    msg = input("> ")    

    if(msg != ''):
        
        socket.send(msg.encode())

        response = socket.recv(1024)

        print("> " + response.decode())

    else:
        print("tell us what us want !")
