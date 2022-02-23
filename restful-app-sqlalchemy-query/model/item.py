from db import db

# Extending from db.Model
class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # Sqlalchemy Takes care of joins

    def __init__(self,name,price,store_id):
        # these attr name should match the alchemy columns
        self.name = name
        self.price = price
        self.store_id = store_id
        # can have other properties that dont have mapping and wont be saved

    # Leverage returning json object representation to be used by flask resource
    def json(self):
        return {'name': self.name , 'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        # ItemModel extends db.Model which has query and filter builders
        item = cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name= :name LIMIT 1
        if item:
            print(f'Printing fetched item on name = {name} | ITEM : {item.name} - {item.price}')
        return item
        # return ItemModel.query.filter_by(name=name).filter_by(id=1)

    def insertOrUpdate(self):
        # alchemy takes care of the object and knows to insert or update
        db.session.add(self)
        db.session.commit()  # can add multiple objects in a session and commit

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()