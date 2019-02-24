import random, logging
from blueprints import db
from flask_restful import fields


class Ratings(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    cuisines = db.Column(db.String(50))
    average_cost_for_two = db.Column(db.Integer)
    currency = db.Column(db.String(6))
    user_rating = db.Column(db.String(6))


    #unique=True kalau mau atribut nya unik, yang lain ga boleh ada yang sama

    response_field = {
        'id' : fields.Integer,
        'name' : fields.String,
        'location' : fields.String,
        'cuisines' : fields.String,
        'average_cost_for_two' : fields.Integer,
        'currency' : fields.String,
        'user_rating' : fields.String
    }

    def __init__(self, id, name, location, cuisines, average_cost_for_two, currency, user_rating):
        self.id = id
        self.name = name
        self.location = location
        self.cuisines = cuisines
        self.average_cost_for_two = average_cost_for_two
        self.currency = currency
        self.user_rating = user_rating

    def __repr__(self): #initiate table model
        return '<makanan %r>' % self.id #the __repr__ must have a string type as return
