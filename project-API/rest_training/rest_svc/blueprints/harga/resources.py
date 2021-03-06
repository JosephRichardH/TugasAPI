import requests, json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal
from flask_jwt_extended import jwt_required
from blueprints import *


bp_harga = Blueprint('harga', __name__)
api = Api(bp_harga) #daftar ke Api

class Harga(Resource):
    zomato_host = 'https://developers.zomato.com/api/v2.1'
    zomato_apikey = '4b63ea47d29600228a3baf3785b91b3b'

    # @jwt_required
    def get(self):

        rq = requests.get(self.zomato_host + '/search', headers={'user-key': self.zomato_apikey}, params={'q':'jakarta'})
        zom = rq.json()
        data = []

        for i in range (int(zom['results_shown'])):
            # harga = int(zom['restaurants'][i]['restaurant']['average_cost_for_two'])
            # harga = "{:,}".format(harga)
            x = {
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
            
        parser = reqparse.RequestParser()
        
        parser.add_argument('maks_harga', location='args', type=int, default=1)
        
        args=parser.parse_args()
        
        rows = []

        for i in range(len(data)):
            if data[i]['perkiraan_harga_2orang'] <= args['maks_harga']:
                rows.append(data[i])
        if rows == []:
            return "Restoran tidak ditemukan", 200, {'Content-Type': 'application/json'}
        return rows, 200, { 'Content-Type': 'application/json' }
        
        # return data

api.add_resource(Harga, '')
