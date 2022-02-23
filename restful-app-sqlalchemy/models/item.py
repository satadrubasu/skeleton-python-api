import sqlite3
from db import db

# Extending from db.Model
class ItemModel(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    price = db.Column(db.Float(precision=2))

    def __init__(self,name,price):
        self.name = name
        self.price = price
    # Leverage returning json object representation to be used by flask resource
    def json(self):
        return {'name': self.name , 'price':self.price}

    @classmethod
    def find_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))  # Tuple identification with single element ending in comma
        row = result.fetchone()
        connection.close()
        if row:
            #return cls(row[0],row[1])
             return cls(*row) # argument unpacking

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (self.name, self.price,))
        connection.commit()
        connection.close()

    @classmethod
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.price, self.name,))
        connection.commit()
        connection.close()
