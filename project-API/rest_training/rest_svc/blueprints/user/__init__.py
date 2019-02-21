import random, logging
from blueprints import db
from flask_restful import fields


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_type = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    #unique=True kalau mau atribut nya unik, yang lain ga boleh ada yang sama

    response_field = {
        'id' : fields.Integer,
        'user_type' : fields.String,
        'name' : fields.String,
        'password' : fields.String
    }

    def __init__(self, id, user_type, name, password):
        self.id = id
        self.user_type = user_type
        self.name = name
        self.password = password
       
    def __repr__(self): #initiate table model
        return '<User %r>' % self.id #the __repr__ must have a string type as return
  