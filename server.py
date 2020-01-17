import socket,requests,json

from backend import Backend

from threading import Thread

#DEFINING CONSTANTS

HOST = '127.0.0.1'

MAX_CONNECTION_ALLOWED = 10

PORT = 8888


#CREATE A SOCKET

def socket_provider(host , port):

    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    socket_instance.bind((host, port))

    socket_instance.listen()

    return socket_instance


#CREATING THREADS

def thread_provider(socket_instance , number_of_connection_to_create):

    for i in range(0,number_of_connection_to_create):

        Thread(target = work , args = (socket_instance,)).start()


#SERVER JOB

def work(socket_instance):

    backend_instance  = Backend()

    connection, address = socket_instance.accept()

    while True:

        client_request = connection.recv(1024)
        
        client_request = client_request.decode()

        if client_request != "":

            print("client sent : " + client_request )

            json_response = backend_instance.dispatcher(client_request)

            nature  = json_response['nature']

            del(json_response['nature'])

            if nature == 'error':

                response = json_response['error_msg']

#HANDLING AUTHENTICATION 

            if nature == 'authentication':

                login = json_response['login']

                password = json_response['password']

                response = backend_instance.authenticate(login , password)

# HANDLING ROUTES TO LDD

            if(nature == 'create_database'):

                response = backend_instance.create_database(json_response['database_name'])

            if(nature == 'create_table'):

                response = backend_instance.create_table(json.dumps(json_response))

            if(nature == 'create_user'):

                response = backend_instance.create_user(json.dumps(json_response))

            if(nature == 'drop_database'):

                response = backend_instance.drop_database(json_response['database_name'])

            if(nature == 'drop_table'):

                response = backend_instance.drop_table(json_response['table_name'])

            if(nature == 'use'):

                response = backend_instance.use(json_response['database_name'])


#HANDLING ROUTES TO LMD

            if(nature == 'insert'):

                response = backend_instance.insert(json.dumps(json_response))

            if(nature == 'update'):

                response = backend_instance.update(json.dumps(json_response))

            if(nature == 'delete'):

                response = backend_instance.delete(json.dumps(json_response))

# HANDLING ROUTES TO LED

            if(nature == 'select'):
                
                response = backend_instance.select(json.dumps(json_response))

        connection.send(response.encode())



#LAUUNCHING THE SERVER

given_socket = socket_provider(HOST , PORT)

thread_provider(given_socket , MAX_CONNECTION_ALLOWED)