import sqlite3
from flask_restful import Resource

class Health(Resource):
    def get(self):
        return {"Status":"Alive"},201