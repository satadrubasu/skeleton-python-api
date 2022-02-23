import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)  # Tuple identification with single element ending in comma
        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()
        return {'items':items} # Ensure Json Object encapsulates the list

####### RESTFul RESOURCE -- Item #########
class Item(Resource):
    parser = reqparse.RequestParser()
    ##parser will only pick the price element
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price cannot be left blank"
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
        item = ItemModel(name, parsed_data['price'])
        try:
            item.insert()
        except:
            return{"message":"An Error occured inserting the item"},500 # Internal server error
        ## Returning JSON Object
        return item.json() , 201 # Created

    def delete(self,name):
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()
        return {'message':'Item deleted'}

    def put(self,name):
        parsed_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name,parsed_data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message":"Error occured inserting the item"},500
        else:
            try:
                updated_item.update() # note using the item obj ref and not the updated item
            except:
                return {"message":"Error occured inserting the item"},500
        return updated_item.json()
        # item = next(filter(lambda x: x['name'] == name, items),None)
        # if item is None:
        #     item = {'name':name ,'price': parsed_data['price'] }
        #     items.append(item)
        # else:
        #     item.update(parsed_data)
        #     return item

