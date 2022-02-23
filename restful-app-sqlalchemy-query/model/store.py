from db import db

# Extending from db.Model
class StoreModel(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))

    # Back reference let a store see many items from the table items linked to it.
    # Figures out many to one relationship automatically hence items is a list.
    # (lazy = dynamic | self.items.all() ,  otherwise , self.items )
    items = db.relationship('ItemModel',lazy='dynamic')

    def __init__(self,name):
        # these attr name should match the alchemy columns
        self.name = name
        # can have other properties that dont have mapping and wont be saved

    # Leverage returning json object representation to be used by flask resource
    # self.items.all() is a query builder. So only when json() called the related items are loaded.
    # this along with lazy = dynamic , lets the create model operation be lean
    def json(self):
        return {'name': self.name , 'items':[item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls,name):
        # ItemModel extends db.Model which has query and filter builders
        store = cls.query.filter_by(name=name).first()  # SELECT * FROM items WHERE name= :name LIMIT 1
        if store:
            print(f'Printing fetched item on name = {name} | ITEM : {store.name}')
        return store
        # return ItemModel.query.filter_by(name=name).filter_by(id=1)

    def save_to_db(self):
        # alchemy takes care of the object and knows to insert or update
        db.session.add(self)
        db.session.commit()  # can add multiple objects in a session and commit

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()