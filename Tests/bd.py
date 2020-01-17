import json

def insert(dumped_data):

    database_in_use = 'data.json'
    
    data_to_insert ={}

    #Récupération des données passées en paramètres

    loaded_data=json.loads(dumped_data)

    table_name = loaded_data['table']

    #COmpter le nombre d'éléments dans la table pour l'id

    database = None

    with open(database_in_use,'r') as database_file:

        database = json.load(database_file)

        id = len(database[table_name])

        fields = loaded_data['fields']

        values = loaded_data['values']

        table_length = len(fields)

        for i in range(0,table_length):

            data_to_insert[fields[i]] = values[i]
           
        print(data_to_insert)

        database[table_name][id+1]=data_to_insert
                   
          
    with open(database_in_use,'w') as updated_database:
        
        json.dump(database,updated_database)