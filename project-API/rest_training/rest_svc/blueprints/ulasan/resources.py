import logging, json, requests
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required, get_jwt_claims

bp_review = Blueprint('review', __name__)
api = Api(bp_review)

class ReviewResource(Resource): 
    zomato_host = 'https://developers.zomato.com/api/v2.1'
    zomato_apikey = '4b63ea47d29600228a3baf3785b91b3b'

    def __init__(self):
        pass    
        
    def get_restos(self):
        #get the restaurants data from the remote API
        rq = requests.get(self.zomato_host + '/search', headers={'user-key': self.zomato_apikey}, params={'q':'jakarta'})
        zom = rq.json()
        data = []
        for i in range (int(zom['results_shown'])):
            x={
                'id': zom['restaurants'][i]['restaurant']['id'],
                'nama': zom['restaurants'][i]['restaurant']['name'],
                'lokasi': {
                    'alamat': zom['restaurants'][i]['restaurant']['location']['address'],
                    'daerah': zom['restaurants'][i]['restaurant']['location']['locality'],
                    'kota': zom['restaurants'][i]['restaurant']['location']['city']
                },
                'masakan': zom['restaurants'][i]['restaurant']['cuisines'],
                'perkiraan_harga_2orang': zom['restaurants'][i]['restaurant']['average_cost_for_two'],
                'mata_uang': zom['restaurants'][i]['restaurant']['currency'],
                'rating': {
                    'bintang': zom['restaurants'][i]['restaurant']['user_rating']['aggregate_rating'],
                    'ulasan': zom['restaurants'][i]['restaurant']['user_rating']['rating_text']
                }
            }
            data.append(x)
        return data
            
    @jwt_required
    def post(self):
        data = self.get_restos()

        #Get the reviews from user
        parser = reqparse.RequestParser()
        parser.add_argument('nama restaurant', location='json', required=True)
        parser.add_argument('bintang', location='json')
        parser.add_argument('ulasan', location='json')
        parser.add_argument('reviewer', location='json')
        args = parser.parse_args() #this becomes str_serialized
        if args['reviewer'] == "anonymous":
            post_by = "anonymous"
        else:
            post_by = get_jwt_claims()['name']
        #get the restaurant detail from data in variable data, use name to find the required restaurant
        resto = None
        for i in range(len(data)):
            if args['nama restaurant'].lower() in data[i]['nama'].lower():
                resto = data[i]
                ulasan_new = Reviews(resto['nama'], args['bintang'], args['ulasan'], post_by)
                db.session.add(ulasan_new) #insert the input data into the database
                db.session.commit() #commit ga ad argument
                break
        if resto is None:
            return 'Restaurant dengan nama tersebut tidak ditemukan', 200, {'Content-Type': 'application/json'} 
        return ulasan_new, 200, {'Content-Type': 'application/json'}
    
    @jwt_required
    def put(self):
        data = self.get_restos()
        #Get the reviews from user
        parser = reqparse.RequestParser()
        parser.add_argument('nama restaurant', location='json', required=True)
        parser.add_argument('bintang', location='json')
        parser.add_argument('ulasan', location='json')
        parser.add_argument('reviewer', location='json')
        args = parser.parse_args() 
        if args['reviewer'] == "anonymous":
            post_by = "anonymous"
        else:
            post_by = get_jwt_claims()['name']
        resto = None
        for i in range(len(data)):
            if args['nama restaurant'].lower() in data[i]['nama'].lower():
                resto = data[i]
                ulasan_update = Reviews(resto['nama'], args['bintang'], args['ulasan'], post_by)
                db.session.commit() 
                break
        if resto is None:
            return 'Restaurant dengan nama tersebut tidak ditemukan', 200, {'Content-Type': 'application/json'} 
        return ulasan_update, 200, {'Content-Type': 'application/json'}
    
    @jwt_required   
    def delete(self, id):
        data = self.get_restos()
        #Get the reviews from user
        parser = reqparse.RequestParser()
        parser.add_argument('nama restaurant', location='json', required=True)
        parser.add_argument('bintang', location='json')
        parser.add_argument('ulasan', location='json')
        args = parser.parse_args() 
        resto = None
        for i in range(len(data)):
            if args['nama restaurant'].lower() in data[i]['nama'].lower():
                resto = data[i]
                if args['bintang'] == 'abort':
                    args['bintang'] = 0
                if args['ulasan'] == 'abort':
                    args['ulasan'] = ''
                ulasan_update = Reviews(resto['nama'], args['bintang'], args['ulasan'])
                db.session.commit() 
                break
        if resto is None:
            return 'Restaurant dengan nama tersebut tidak ditemukan', 200, {'Content-Type': 'application/json'} 
        return 'Reviews have been deleted', 200, {'Content-Type': 'application/json'}
        
    def patch(self):
        return 'Not yet implemented', 501

api.add_resource(ReviewResource, '')
