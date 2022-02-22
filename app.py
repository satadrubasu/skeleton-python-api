from flask import Flask,jsonify,request , render_template

app = Flask(__name__)
## Note 1: jsonify method converts python dict to json string
##         but stores is a list so jsonify({'stores':stores})
## Note 2: json always uses double quotes

## Note 3: from flask import request : access request object

#### stores in memory for e.g
stores = [
    {
        'name':'Home Store',
        'items': [
            {
                'name':'Wallpaper',
                'price':'1099.00'
            }
        ]

    }
]


####

@app.route('/test')
def test_up():
    return "Flask App is Up !!"

@app.route('/')
def home():
    return render_template('index.html')

##### CREATE-STORE -
# POST /store data: {name:}
@app.route('/store',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)
    pass

# GET /store/<string:resourceName>
@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    for a_store in stores:
        if a_store['name'] == name:
            return jsonify(a_store)
    return jsonify({'message':'store not found'})
    pass

# GET /store
@app.route('/store', methods=['GET'])
def get_all_stores():
    return jsonify({'stores':stores})

# POST /store/<string:name>/item  data: {name:,price:}
@app.route('/store/<string:name>/item',methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'Store not found'})





# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_store_items(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message': 'store not found'})

app.run(port=5000)