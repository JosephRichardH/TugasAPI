import random, logging
from blueprints import db
from flask_restful import fields


class Restos(db.Model):
    __tablename__ = "resto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=True)
    harga = db.Column(db.Integer, nullable=True)
    lokasi = db.Column(db.String(255), nullable=True)
    makanan = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ulasan = db.Column(db.String(255), nullable=True)
    
    #unique=True kalau mau atribut nya unik, yang lain ga boleh ada yang sama

    response_field = {
        'id' : fields.Integer,
        'nama' : fields.String,
        'harga' : fields.Integer,
        'lokasi' : fields.String,
        'makanan' : fields.String,
        'rating' : fields.Float,
        'ulasan' : fields.String
    }

    def __init__(self, id, harga, lokasi, makanan):
        self.id = id
        self.harga = harga
        self.lokasi = lokasi
        self.makanan = makanan
        self.rating = rating
        self.ulasan = ulasan
       
    def __repr__(self): #initiate table model
        return '<Restaurant %r>' % self.id #the __repr__ must have a string type as return
  