import socket,requests,json

HOST = '127.0.0.1'

PORT = 8889

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.bind((HOST, PORT))

socket.listen()
   
connection, address = socket.accept()

while True:

        client_request = connection.recv(1024)
        
        client_request = client_request.decode()

        if client_request != "":

            print("client sent : " + client_request )

            api_response = requests.get(" http://127.0.0.1:5000/" + client_request)

            json_response = json.loads(api_response.text)

            nature  = json_response['nature']

            del(json_response['nature'])

# HANDLING ROUTES TO LDD

            if(nature == 'create_database'):

                api_response = requests.get(" http://127.0.0.1:5000/create_database/" + json_response['database_name'])

            if(nature == 'create_table'):

                api_response = requests.get(" http://127.0.0.1:5000/create_table/" + json_response['table_name'])

            if(nature == 'drop_database'):

                api_response = requests.get(" http://127.0.0.1:5000/drop_database/" + json_response['database_name'])

            if(nature == 'drop_table'):

                api_response = requests.get(" http://127.0.0.1:5000/drop_table/" + json_response['table_name'])

            if(nature == 'use'):

                api_response = requests.get(" http://127.0.0.1:5000/use/" + json_response['database_name'])


#HANDLING ROUTES TO LMD

            if(nature == 'insert'):

                api_response = requests.get(" http://127.0.0.1:5000/insert/" + json.dumps(json_response))

            if(nature == 'update'):

                api_response = requests.get(" http://127.0.0.1:5000/update/" + json.dumps(json_response))

            if(nature == 'delete'):

                api_response = requests.get(" http://127.0.0.1:5000/delete/" + json.dumps(json_response))

# HANDLING ROUTES TO LED

            if(nature == 'select'):
                
                print(json_response)

                api_response = requests.get(" http://127.0.0.1:5000/select/" + json.dumps(json_response))

                print(json.dumps(json_response))

            connection.send((api_response.text).encode())
