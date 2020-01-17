#This is the class where all methods the API use are going to be put

import os

from flask import json

class Backend:

    DATABASE_IN_USE = ''

    DATABASE_DIRECTORY_PATH = "Databases/"

    CURRENT_USER = ''

# LDD -----------------------------------------------------------------------------------

    #Creating a database

    def create_database(self,db_name):

        try:
            f = open(self.DATABASE_DIRECTORY_PATH + db_name + ".json" , "r")
            
            return "Database " + db_name + " already exists !"
        
        except :

            f = open(self.DATABASE_DIRECTORY_PATH + db_name + ".json" , "w+")

            config = open(self.DATABASE_DIRECTORY_PATH + "config.json" , "a+")

            temporar_unused_database = self.CURRENT_USER + '-' + db_name + '-' + 'CREATION' 

            config.write('\n')

            config.write(temporar_unused_database)

            config.close()

            return "database '" + db_name + "' created successfully !"

        finally:

            f.close()
    
    
    # Creating a table

    def create_table(self,table_data):

        if self.DATABASE_IN_USE == '':

            return "No database selected !"

        table_data = json.loads(table_data)

        # Writing data on config file

        config_file = open(self.DATABASE_DIRECTORY_PATH + "config.json" , "a+")

        full_table_name = self.CURRENT_USER + '-' +  self.DATABASE_IN_USE + '-' + table_data['table_name']

        data = full_table_name

        for field in table_data['fields']:

            data+='-'

            data += field

        print(data)

        config_file.write('\n')

        config_file.write(data)
  
        config_file.close()

        #Editing real database structure

        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + ".json" , "r") as database_file:
           
            try:
               
                db_data = json.load(database_file)

            except:
                
                db_data = {}

            finally:
                
                db_data[table_data['table_name']] = {}

        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + ".json" , "w") as updated_database_file:
            
            json.dump(db_data,updated_database_file)

        return "Table " + table_data['table_name'] + " has been created successfully !"

    #Create a user

    def create_user(self,user_credentials):

        user_credentials = json.loads(user_credentials)

        login = user_credentials['login']

        password = user_credentials['password']
        
        user_data = login + "-" + password

        with open(self.DATABASE_DIRECTORY_PATH + 'users.txt' , 'a') as user_file:

            user_file.write('\n')

            user_file.write(user_data)

        return "The user has been recorded successfully"

    # Dropping a database

    def drop_database(self,db_name):
        
        if os.path.exists(self.DATABASE_DIRECTORY_PATH + db_name + ".json"):
           
            os.remove(self.DATABASE_DIRECTORY_PATH + db_name + ".json")
           
            return "database " + db_name + " deleted successfully"
        
        else:
            return "database " + db_name + " doesn't exist"

    #Dropping a table

    def drop_table(self,table_name):

        if self.DATABASE_IN_USE == '':

            return "No database selected !"

        return "dropping table " + table_name + "..."

    #Use a database

    def use(self, db_name):

        f = open(self.DATABASE_DIRECTORY_PATH + "unecessary")

        #check if database exists
       
        try:

            f = open(self.DATABASE_DIRECTORY_PATH + db_name + ".json" , "r")

            current_user_databases = self.get_databases_of_user(self.CURRENT_USER)

            if(db_name not in current_user_databases):

                return "database '" + db_name + "' doesn't exist !"    

            else :
                self.DATABASE_IN_USE = db_name

                return "database '" + db_name + "' in use!"

        except :

            return "database '" + db_name + "' doesn't exists !"

        finally:

            f.close()

# END LDD -----------------------------------------------------------------------------------


#LMD ----------------------------------------------------------------------------------------

    #Insert data into database

    def insert(self,request_data):
        
        if self.DATABASE_IN_USE == '':
        
            return "No database selected !"

        #Load request data

        request_data = json.loads(request_data)

        table_name = request_data['table']

        fields = request_data['fields']
        
        values = request_data['values']

        #Check if the table user wants to insert into, truly exists

        existing_tables = self.get_tables_of(self.DATABASE_IN_USE)

        if table_name not in existing_tables:
            
            return table_name + ' doesn\'t exists in the current database !'
       
       #Check if fields the user want to insert into, truly exist
        
        existing_fields = self.get_fields_of(table_name)

        for field in fields:
            
            if field not in existing_fields:

                return  'A field named ' + field + " doesn\'t exist in the table !"

        #Take into account the case when the user just give some fields

        for field in existing_fields:
            
            if field not in fields:

                fields.append(field)

                values.append("Null")
   
    #Compter le nombre d'éléments dans la table pour l'id

        database = None

        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE +'.json','r') as database_file:

            database = json.load(database_file)

            print(database[table_name])

            id = len(database[table_name])

            table_data = database[table_name]

            #Check if there's the same number of fields and values

            if len(fields) != len(values):
                
                return 'There must be as much fields as values !'

            table_length = len(fields)

            #Creating the structure to add in the database

            data_to_insert = {}

            for i in range(0,table_length):

                data_to_insert[fields[i]] = values[i]
            
            database[table_name][str(id + 1)] = data_to_insert
                   
        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE +'.json','w') as updated_database :
            
            json.dump(database,updated_database)

        return "The record has been inserted successfully"


    #Updating items

    def update(self,request_data):
        
        if self.DATABASE_IN_USE == '':
            
            return "No database selected !"

        #récupérer les données pilotant la modification
        else:

            loaded_data = json.loads(request_data)

            field_value = loaded_data['field_value']

            print(loaded_data)

            #Field to update and its new value

            field_to_update = field_value[0]

            value_of_updated_field = field_value[1]


            #récupérer l'id du champ à modifer

            given_id = loaded_data['id']

            given_id = int(given_id)

            #Ouvrir la base de données

            with open (self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + '.json' ,'r') as file_data :
                
                #récupérer toutes données de la base

                loaded_database = json.load(file_data)

                #récupérer les données de la table qui est concernée

                table_name =loaded_data['table']
                
                table_data = loaded_database[table_name]

                #vérifier si nous avons un seul élément à modifier

                if given_id != -1 and given_id <= len(table_data):

                    data =  table_data[str(given_id)]

                    data[field_to_update] = value_of_updated_field

        #vérifier si l'id est supérieur au nombres de champs
        
                elif(given_id > len(table_data)):
                
                    print("Cannot be update")        
        
        #on applique le update à tous les champs de la table correspondante
        
                else:

                    for i in range(1,len(table_data) + 1):

                        data =  table_data[str(i)]

                        data[field_to_update] = value_of_updated_field

            #Enregistrer les modifications

            with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + '.json' , 'w') as updated_database:

                    json.dump(loaded_database,updated_database)

        return "Record updated successfully..."

        #Deleting items

    def delete(self,request_data):
        
        if self.DATABASE_IN_USE == '':
            
            return "No database selected !"

        loaded_data = json.loads(request_data)

        print(loaded_data)

        given_id =loaded_data['id']

        print(given_id)

        given_id = int(given_id)

        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + '.json','r') as file_data:

            loaded_database = json.load(file_data)

            table_name =loaded_data['table']
            
            table_data = loaded_database[table_name]

            if given_id != -1 and given_id <= len(table_data):

                data = table_data[str(given_id)]

                # suppression des data de la table

                data.clear()

                # puis je delete l'id correspondant
                del table_data[str(given_id)]

            elif given_id == -1:

                loaded_database[table_name] = {}
                
            else:

                print("Cannot be deleted")        

        with open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + '.json','w') as updated_database:

                json.dump(loaded_database,updated_database)

        return "Data successfully deleted!"

#END LMD ------------------------------------------------------------------------------------


# LED -----------------------------------------------------------------------------------

    #Fetch data from database

    def select(self,request_data):

        if self.DATABASE_IN_USE == '':

            return "No database selected !"

        request_data = json.loads(request_data)

        #load the database

        f = open(self.DATABASE_DIRECTORY_PATH + self.DATABASE_IN_USE + ".json",'r')
      
        data = json.load(f)

        table_name = request_data['table']
        
        fields = request_data['fields']

        #verify if the table truly exist in the database

        existing_tables = self.get_tables_of(self.DATABASE_IN_USE)

        if table_name not in existing_tables:

            return 'table ' + table_name + 'doesn\'t exist in the current database !'

        #verify if fields given truly exist in the table 

        existing_fields = self.get_fields_of(table_name)

        for field in fields:
            
            if field not in existing_fields:

                return field + " doesn\'t exist in the table " + table_name

        #verify if there are data in the table

        data = data[table_name]

        if data == {}:
            
            return "Table " + table_name + " has no record !"

        response = ""

        for id in data:

            response+='id: '+ id + '\n'
                        
            current_tuple = data[id]

            for current_tuple_key in current_tuple:
                
                if current_tuple_key in fields:

                    response+= str(current_tuple_key).upper() + ' : ' + current_tuple[current_tuple_key]
                
                response+="\n"

            response+="-----------------\n"

        return response

#END LED -----------------------------------------------------------------------------------



#Other -------------------------------------------------------------------------------------


    #GET USER DATABASES

    def get_databases_of_user(self,user_name):

        config_file = open(self.DATABASE_DIRECTORY_PATH + 'config.json' , 'r')
       
        lines = config_file.readlines()

        databases = []

        for line in lines:

            line.replace("\"",'')

            data = line.split('-')            

            if data[0] == user_name :

                databases.append(data[1])

        return databases

    #GET DATABASE FIELDS

    def get_tables_of(self,database_name):

        config_file = open(self.DATABASE_DIRECTORY_PATH + 'config.json' , 'r')
       
        lines = config_file.readlines()

        tables = []

        for line in lines:

            line.replace("\"",'')

            data = line.split('-')            

            if data[1] == database_name :

                tables.append(data[2])
        
        return tables

    #GET TABLE FIELDS

    def get_fields_of(self , table):
        
        if self.DATABASE_IN_USE == '':
            
            return "No database selected !"

        config_file = open(self.DATABASE_DIRECTORY_PATH + 'config.json' , 'r')
       
        lines = config_file.readlines()

        for line in lines: 

            line.replace("\"",'')

            data = line.split('-')            

            if( data[0] == self.CURRENT_USER and data[1] == self.DATABASE_IN_USE and data[2] == table):

                #removing the user, the database name and the table name

                data.pop(0)

                data.pop(0)

                data.pop(0)

                last_item = data[len(data)-1].strip()

                data.pop(len(data) - 1)

                data.append(last_item)

                config_file.close()

                return data

        return None

    #SYNTAX CHECKER

    def validate(self,query):

        return "this is where the presumed SQL query : '" + query + "' will be validated ! "


    #AUTHENTICATION

    def authenticate(self , login , password):

        user_file = open(self.DATABASE_DIRECTORY_PATH + 'users.txt' , 'r')

        users = user_file.readlines()

        for user in users:

            current_user_data = user.split('-')

            current_user_login = current_user_data[0]

            current_user_password = current_user_data[1]

            current_user_password = current_user_password.strip()

            if current_user_login == login and current_user_password == password:

                self.CURRENT_USER = login

                return "true" 

        return "false"


    #SEMANTIC ANALYSER 

    def dispatcher(self , user_input):  
        
        requete = user_input
      
        #declaration
      
        database ={}
      
        table = {}
      
        select ={}
      
        insert = {}
      
        update = {}

        show = {}
        
        user =  {}
        value = []

        requete=requete.lower()
      
        tabRequet=[]
      
        champ = []
      
        mot= ""
      
        j=0
      
        k=0
        
        long = len(requete)

        #stockage de la requete dans un tableau
       
        for i in range (0,long):

            if((requete[i] != " ") and (requete[i] != "=")):

                if(requete[i] != "("):

                    if(requete[i] != ")"):

                        if(requete[i] != "'" ):

                            if(requete[i] !="," ):

                                mot = mot + requete[i]
            else:

                tabRequet.append(mot)

                mot = ""

                j=j+1


        #GESTION DES AUTHENTIFICATIONS
        if(tabRequet[0] == "credentials"):
            
            authentication = {
            
                'nature': "authentication",
            
                'login': tabRequet[1],
            
                'password': tabRequet[2]
            }     

            return authentication

        #GESTION DES REQUETES CREATE 

        elif(tabRequet[0]=="create"):
        
            if(tabRequet[1]=="database"):
                
                database = {

                    'nature': "create_database",

                    'database_name': tabRequet[2]
                }

                return database

            elif(tabRequet[1]=="user"):
                
                user = {

                    'nature': "create_user",

                    'login': tabRequet[2],

                    'password': tabRequet[5]
                }

                return user

            elif(tabRequet[1]=="table"):
        
                for i in range (3,len(tabRequet)):
        
                    champ.append(tabRequet[i])
        
                table = {

                    'nature': "create_table",

                    'table_name': tabRequet[2],

                    'fields': champ
                }

                return table
            
            else:

                return {

                    'nature':'error',

                    'error_msg':'Check create command syntax'
                } 

        #GESTION DES REQUETES DROP

        elif(tabRequet[0]=="drop"):
        
            if(tabRequet[1]=="database"):
        
                database = {

                    'nature': "drop_database",

                    'database_name': tabRequet[2]
                }

                return database

            elif(tabRequet[1]=="table"):
        
                table = {

                    'nature': "drop_table",

                    'table_name': tabRequet[2]
                }

                return table

            else:
                
                return {

                    'nature':'error',

                    'error_msg':'Check drop command syntax'
                }

        #GESTION DES REQUETES SELECT
        
        elif(tabRequet[0]=="select"):

            table_name = tabRequet[(len(tabRequet)-1)]

            if(tabRequet[1]=="*"):

                # Get all fields of the table

                fields = self.get_fields_of(table_name)

                if fields == None:
                    
                    return {
                        
                        'nature':'error',

                        'error_msg': 'table ' + table_name + ' doesn\'t exists in the currently selected database'
                    }

                select = {

                    'nature': "select",

                    'table':table_name,

                    'fields': fields

                }

            else:

                for i in range (1,(len(tabRequet)-1)):

                    if(tabRequet[i] != "from"):

                        champ.append(tabRequet[i])

                select = {

                    'nature': "select",

                    'table': table_name,

                    'fields':champ
                }

            return select

        #GESTION DES REQUETES INSERT

        elif(tabRequet[0] == "insert"):
         
            for i in range (3,(len(tabRequet)-1)):

                if(tabRequet[i] == "values"):
                
                    break

                else:

                    k=k+1

                    champ.append(tabRequet[i])

            for i in range ( ( 4 + k ),( len(tabRequet) )):

                value.append(tabRequet[i])

            insert = {

                'nature': "insert",

                'table': tabRequet[2],

                'fields':champ,

                'values': value
            }

            return insert

        elif (tabRequet[0]=="update"):

            for i in range (3,len(tabRequet)):

                if(tabRequet[i] == "where"):

                    break

                else:

                    k = k + 1

                    champ.append(tabRequet[i])

            if((k+3) == len(tabRequet)):

                update = {

                'nature': "update",

                'table': tabRequet[1],

                'field_value': champ,

                'id': -1
                }

            else:

                update = {

                'nature': "update",

                'table': tabRequet[1],

                'field_value':champ,

                'id': tabRequet[(len(tabRequet)-1)],

                }

            return update

        #Gestion des requetes delete

        elif(tabRequet[0]=="delete"):

            for i in range (3,(len(tabRequet))):

                if((tabRequet[i]!="and") and (tabRequet[i]!="where")):
                
                    champ.append(tabRequet[i])
    
            if(len(champ)!=0):
        
                delete = {
                    
                    'nature': "delete",

                    'table': tabRequet[2],
                    
                    'id':champ[1]

                    }
            else:

                delete = {

                    'nature': "delete",

                    'table': tabRequet[2],
                
                    'id':-1

                }

            return delete
        #GESTION DES REQUETES USE

        elif(tabRequet[0] == "use"):

            data = {

                'nature' : "use",

                'database_name':tabRequet[1]
            }

            return data
        # GESTION DES REQUETES SHOW
        elif(tabRequet[0] == "show"):

            show = {

                'nature' : "show",

                'table':"tables"
            }
            return show
        else:
                return {

                    'nature':'error',

                    'error_msg':'Command doesn\'t exist'
                }

