import requests, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
######
from blueprints import db
from . import * #ambil init.py
###
from flask_jwt_extended import jwt_required

###S

bp_semua = Blueprint('semua', __name__)
api = Api(bp_semua) #daftar ke Api

class Semua(Resource):
    zomato_host = 'https://developers.zomato.com/api/v2.1'
    zomato_apikey = '4b63ea47d29600228a3baf3785b91b3b'

    # @jwt_required
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('user-key', location='args', default=None)
        # args = parser.parse_args()

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
         
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='json')
        parser.add_argument('nama', location='json')
        parser.add_argument('harga', location='json')
        parser.add_argument('lokasi', location='json')
        parser.add_argument('makanan', location='json')
        parser.add_argument('rating', location='json')
        parser.add_argument('ulasan', location='json')
        args = parser.parse_args() #this becomes str_serialized
        # if args['user_type'] is None:
        #     args['user_type'] = 'publik'
        #     user_new = Users(None, args['user_type'], args['name'], args['password'])
        resto_new = Restos(args['id'], args['nama'], args['harga'], args['lokasi'], args['makanan'], args['rating'], args['ulasan'])
        db.session.add(user_new) #insert the input data into the database
        db.session.commit() #commit ga ad argument
        return marshal(user_new, Users.response_field)
   

api.add_resource(Semua, '')
