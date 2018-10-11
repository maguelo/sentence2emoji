'''

https://app.swaggerhub.com/apis-docs/Maguelo/sentence2emoji/0.1

@author: Miguel Maldonado
'''

from flask import Flask
from flask_restful import Api, Resource, reqparse
from sentence2emoji.model import SentimentAnalysis
from sentence2emoji.controller import controller
import os
from definitions import MODEL_PATH

app = Flask(__name__)
api = Api(app)

users = {}
users["Nicholas"]={"emoji":"😁"}
users["Elvin"]={"emoji":None}
users["Jass"]={"emoji":None}
    
PATH_MODEL_FILE = os.path.join(MODEL_PATH,"model.json")
PATH_WEIGHTS_FILE =os.path.join(MODEL_PATH,"model.h5")

def generateResponse(response,code):
    return {"response":response},code

class Bot(Resource):
    def __init__(self):
        self.model = SentimentAnalysis.getInstance(PATH_MODEL_FILE,PATH_WEIGHTS_FILE)
        
        
    def get(self, name):        
        if(name in users.keys()):
            return generateResponse(users[name], 200)
        return generateResponse("User not found", 404)

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("sentence")
        args = parser.parse_args()
        
        if not name in users.keys():
            return generateResponse("User with name {} not exists".format(name), 400)
                    
        response = controller(args["sentence"], name,users,self.model)
                
        return generateResponse(response, 200)

    def put(self, name):        
        if name in users.keys():
            return generateResponse("User already exists", 409)
        
        users[name]={"emoji":None}
        
        return generateResponse("Add user {} to database".format(name), 201)

    def delete(self, name):
        del users[name]
        return generateResponse("User {} is deleted.".format(name), 200)
      

api.add_resource(Bot, "/bot/<string:name>")
if __name__ == "__main__":
    app.run(debug=True)