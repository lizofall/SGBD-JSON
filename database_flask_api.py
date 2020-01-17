from flask import Flask,redirect,json,jsonify,session
from flask_restful import Resource,Api
from backend import Backend
import os,requests

app = Flask(__name__)
# generating a secret key, needed for the sessions
app.secret_key = os.urandom(24)
api = Api(app)

backend_instance = Backend()


 # LDD ------------------------------------------------------------------------------------------------

class Create_database(Resource):
    def get(self,db_name):
        return backend_instance.create_database(db_name)

class Create_table(Resource):
    def get(self,table_data):
        return backend_instance.create_table(table_data)

class Drop_database(Resource):
    def get(self,db_name):
        return backend_instance.drop_database(db_name)


class Drop_table(Resource):
    def get(self,table_name):
        return backend_instance.drop_table(table_name)

class Use(Resource):
    def get(self,db_name):
        return backend_instance.use(db_name)

 # END LDD ----------------------------------------------------------------------------------------------


 # LMD ----------------------------------------------------------------------------------------------

class Insert(Resource):
    def get(self,request_data):
        return backend_instance.insert(request_data)

class Update(Resource):
    def get(self,request_data):
        return backend_instance.update(request_data)


class Delete(Resource):
    def get(self,request_data):
        return backend_instance.delete(request_data)

 # END LMD ----------------------------------------------------------------------------------------------


 # LED ----------------------------------------------------------------------------------------------

class Select(Resource):
    def get(self,request_data):
        return backend_instance.select(request_data)

 # END LED ----------------------------------------------------------------------------------------------


 # OTHER ----------------------------------------------------------------------------------------------


class Validate(Resource):
    def get(self,query):
        return backend_instance.validate(query)

class Home(Resource):
    def get(self,query):
        return backend_instance.dispatcher(query)


#DEFINED ROUTES OF THE API

#Routes to syntax analyser and parser

api.add_resource(Home , '/<query>')
api.add_resource(Validate , '/validate/<query>')

#Routes to LDD

api.add_resource(Create_database , '/create_database/<db_name>')
api.add_resource(Create_table , '/create_table/<table_data>')
api.add_resource(Drop_database , '/drop_database/<db_name>')
api.add_resource(Drop_table , '/drop_table/<table_name>')
api.add_resource(Use , '/use/<db_name>')

#Routes to LMD

api.add_resource(Insert , '/insert/<request_data>')
api.add_resource(Update , '/update/<request_data>')
api.add_resource(Delete , '/delete/<request_data>')

#Route to LED

api.add_resource(Select , '/select/<request_data>')

if(__name__) == "__main__" :
    app.run(debug=True)