import random, logging
from blueprints import db
from flask_restful import fields

class Reviews(db.Model):
    __tablename__ = "review"  
    nama_restaurant = db.Column(db.String(255), nullable=True, primary_key=True)  
    bintang = db.Column(db.Float, nullable=False)
    ulasan = db.Column(db.String(255), nullable=False)
    post_by = db.Column(db.String(255), nullable=False)

    response_field = {
        'nama_restaurant' : fields.String, 
        'bintang' : fields.Float,
        'ulasan' : fields.String,
        'post_by' : fields.String
    }

    def __init__(self, nama_restaurant, bintang, ulasan, post_by):
        self.nama_restaurant = nama_restaurant
        self.bintang = bintang
        self.ulasan = ulasan
        self.post_by = post_by

    def __repr__(self): #initiate table model
        return '<Ulasan %r>' % self.id #the __repr__ must have a string type as return
  