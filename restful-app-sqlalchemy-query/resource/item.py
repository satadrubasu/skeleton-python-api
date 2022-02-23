from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from model.item import ItemModel

## Create a Resource Object
##   - implement needful methods on resource get / post etc
## Associate Resource to API Object linked with the app with uris
## Flask restful doesnt need the jsonify - its implicit
## Item and Items will be considered different resource
## return codes.

### Reqparse from flask_restful
## parser = reqparser.RequestParser()



####### RESTFul RESOURCES -- ItemList #########
class ItemList(Resource):
    def get(self):

        itemss = ItemModel.query.all() # Sqlalchemy model query api to do select all
        # itemss is list of all model objects - we need to translate to list of json objects
        jsonTranslatedlistComprehension = [ item.json() for item in itemss]

        # wrap into json obj - list as value to a key.
        return {'items':jsonTranslatedlistComprehension} # Ensure Json Object encapsulates the list

####### RESTFul RESOURCE -- Item #########
class Item(Resource):
    parser = reqparse.RequestParser()
    ##parser will only pick the price element
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every Item needs a store_id"
                        )
    @jwt_required()
    def get(self,name):
        #item = next(filter(lambda x: x['name'] == name , items))
        ## Class method call
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # conver the model to json obj
        return {'message':'Item not Found'} , 404

    def post(self,name):  ## name - from Url
        #if next(filter(lambda x: x['name'] == name,items),None):
        #    msg = f"An item with name '{name}' already exists"
        #    return {'message':msg},400
        ## Class method call
        if ItemModel.find_by_name(name):
            msg = f"An item with name '{name}' already exists"
            return {'message': msg}, 400 # Client side problem


        parsed_data = Item.parser.parse_args()
        ##req_payload = request.get_json()  ## data from request payload
        item = ItemModel(name, parsed_data['price'],parsed_data['store_id'])
        try:
            item.insertOrUpdate()
        except:
            return{"message":"An Error occured inserting the item"},500 # Internal server error
        ## Returning JSON Object
        return item.json() , 201 # Created

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message":"Item Deleted"}


    def put(self,name):
        parsed_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name,**parsed_data)  # Same as below - positional arg
            #item = ItemModel(name, parsed_data['price'], parsed_data['store_id'])
        else:
            item.price = parsed_data['price']
        item.insertOrUpdate()
        return item.json()

