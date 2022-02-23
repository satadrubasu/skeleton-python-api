from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resource.user import UserRegister
from resource.item import Item,ItemList
from resource.store import Store, StoreList

from alive import Health
from db import db


app = Flask(__name__)
app.secret_key = 'externelizeme'
  # Flask_sqlmodification tracker off , but underlying sqlalchemy modify tracker is on.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def create_tables():
    ## Sql alchemy as it scans and knows the metadata of all model and table mapping it auto creates all tables
    db.create_all()


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
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
## Whenever we import a file , all lines execute from that file.
## generally if we dont want to do the runs in the file when getting imported.
## python assigns '__main__' to the __name__ variable when that file is run in python directly
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000)