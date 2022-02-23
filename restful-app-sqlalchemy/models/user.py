import sqlite3
from db import db

# Extend db.Model of SQLAlchemy
class UserModel(db.Model):
    __tablename__ = "users"  # SQLAlchemy specific variable set from db.Model
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(20))

    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        ## always a tuple with single value end with a single comma , else become simple brackets
        result = cursor.execute(query,(username,))
        row = result.fetchone()

        if row:
            #user = cls(row[0],row[1],row[2])
            user = cls(*row) # positional arg , same as above
        else:
            user =None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        ## always a tuple with single value end with a single comma , else become simple brackets
        result = cursor.execute(query,(_id,))
        row = result.fetchone()

        if row:
            #user = cls(row[0],row[1],row[2])
            user = cls(*row) # positional arg , same as above
        else:
            user =None

        connection.close()
        return user
