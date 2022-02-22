from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item,ItemList
from alive import Health

app = Flask(__name__)
app.secret_key = 'externelizeme'
api = Api(app)
## authentication with flask jwt ( Flask-JWT ) creates a new auth endpoint which returns a token
## decorate the resource method with @jwt required
## provide the authenticate and identity method implementation
## Incoming request - /auth and future request header Authorization: JWT <token> & Content-Type = application/json
jwt = JWT(app,authenticate,identity)  ## creates a new endpoint /auth



###### ADDING RESOURCES TO API ########
api.add_resource(Health,'/alive')
api.add_resource(ItemList,'/items')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(UserRegister,'/register')

## Whenever we import a file , all lines execute from that file.
## generally if we dont want to do the runs in the file when getting imported.
## python assigns '__main__' to the __name__ variable when that file is run in python directly
if __name__ == '__main__':
    app.run(port=5000)