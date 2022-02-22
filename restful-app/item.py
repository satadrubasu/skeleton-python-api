import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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

####### RESTFul RESOURCES -- Item #########
class Item(Resource):
    parser = reqparse.RequestParser()
    ##parser will only pick the price element
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="price cannot be left blank"
                        )


    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))  # Tuple identification with single element ending in comma
        row = result.fetchone()
        connection.close()
        if row:
            return {"item" : {'name':row[0],'price':row[1]}}

    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price'],))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name'],))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self,name):
        #item = next(filter(lambda x: x['name'] == name , items))
        ## Class method call
        item = Item.find_by_name(name)

        if item:
            return item
        return {'message':'Item not Found'} , 404

    def post(self,name):  ## name - from Url
        #if next(filter(lambda x: x['name'] == name,items),None):
        #    msg = f"An item with name '{name}' already exists"
        #    return {'message':msg},400
        ## Class method call
        if Item.find_by_name(name):
            msg = f"An item with name '{name}' already exists"
            return {'message': msg}, 400 # Client side problem


        parsed_data = Item.parser.parse_args()
        ##req_payload = request.get_json()  ## data from request payload
        item = {'name': name , 'price': parsed_data['price']}
        try:
            Item.insert(item)
        except:
            return{"message":"An Error occured inserting the item"},500 # Internal server error
        ## Returning JSON Object
        return item , 201 # Created


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

        item = Item.find_by_name(name)
        updated_item = {'name':name,'price':parsed_data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message":"Error occured inserting the item"},500
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message":"Error occured inserting the item"},500
        return updated_item



        # item = next(filter(lambda x: x['name'] == name, items),None)
        # if item is None:
        #     item = {'name':name ,'price': parsed_data['price'] }
        #     items.append(item)
        # else:
        #     item.update(parsed_data)
        #     return item

