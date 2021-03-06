import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from . import *
from blueprints import db
from flask_jwt_extended import jwt_required
import requests
from blueprints.semua import *

bp_rating = Blueprint('rating', __name__)
api = Api(bp_rating)

#using multi route in one class
class RatingResource(Resource):
    # user = Users()
    zomato_host = 'https://developers.zomato.com/api/v2.1'
    zomato_apikey = '4b63ea47d29600228a3baf3785b91b3b'
    
    def __init__(self):
        pass
        
    def get(self):
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

        parser = reqparse.RequestParser()
        parser.add_argument('p', type=int, location='args', default=1)
        parser.add_argument('rp', type=int, location='args', default=5)
        parser.add_argument('rating', type=float, location='args')
        args = parser.parse_args()
        # makanan = marshal(args, Cuisines.response_field)
        #qry = Cuisines.query
#
        hasil = []
        for x in data:
            if float(args['rating']) <= float(x['rating']['bintang']):
                hasil.append(x)
        if hasil == [] :
            return None
        return hasil, 200, {'Content-Type': 'application/json'}
#
#            rumus_offset = args['p'] * args['rp'] - args['rp']
#            qry = Cuisines.query
#            rq = requests.get(data + '/search', headers={'user-key': self.zomato_apikey}, params={'q':cuisine})
#            zom = rq.json()
#            if args['cuisine'] is not None:
#                # qry = qry.filter_by(name=args['name']) #qry that is filtered by name >> for exact name
#                qry = qry.filter(Cuisines.cuisine.like("%"+args['cuisine']+"%")) #for name with this name, and not case sensitive
#            rows = []
#            for row in qry.limit(args['rp']).offset(rumus_offset).all():
#                rows.append(marshal(row, Cuisines.response_field))
#            return rows, 200, {'Content-Type': 'application/json'}
    #    else:
    #        qry = Cuisines.query.get(id) #select * from where id = id
    #        if qry != None:
    #            return marshal(qry, Cuisines.response_field), 200, {'Content-Type': 'application/json'}
                # marshal is converting data from query into the response_field
            # ret = self.user.get_by_id(id)
            # if ret != None:
                # return ret, 200, {'Content-Type': 'application/json'}   
    #        return {'status': 'ID NOT_FOUND'}, 404, {'Content-Type': 'application/json'}
#    @jwt_required #to make with authorization
#    def post(self):
#        parser = reqparse.RequestParser()
#        # parser.add_argument('id', location='json', type=int, required=True)
#        parser.add_argument('name', location='json')
#        parser.add_argument('age', location='json', type=int)
#        parser.add_argument('sex', location='json')
#        parser.add_argument('client_id', location='json', type=int)
#        # parser.add_argument('client_id', location='json', type=int)
#        args = parser.parse_args() #this becomes str_serialized
#        
#        user_new = Users(None, args['name'], args['age'], args['sex'], args['client_id'])
#        db.session.add(user_new) #insert the input data into the database
#        db.session.commit() #commit ga ad argument
#        return marshal(user_new, Users.response_field)
#        # return self.user.add(args), 200, {'Content-Type': 'application/json'}
#
#        #another way
#        # user = User()
#        # user.id = args['id']
#        # user.name = args['name']
#        # user.age = args['age']
#        # user.sex = args['sex']
#        # # user.client_id = args['client_id']
#        # return self.user.add(user.serialize()), 200, {'Content-Type': 'application/json'}
#    @jwt_required
#    def put(self, id):
#        parser = reqparse.RequestParser()
#        parser.add_argument('id', location='json', type=int, required=True)
#        parser.add_argument('name', location='json')
#        parser.add_argument('age', location='json', type=int)
#        parser.add_argument('sex', location='json')
#        parser.add_argument('client_id', location='json', type=int)
#        args = parser.parse_args()
#        qry_user = Users.query.get(id)
#        if qry_user is not None:
#            qry_user.id = args['id']
#            qry_user.name = args['name']
#            qry_user.age = args['age']
#            qry_user.sex = args['sex']
#            qry_user.client_id = args['client_id']
#            db.session.commit()
#            return marshal(qry_user, Users.response_field), 200, {'Content-Type': 'application/json'}
#        return 'Data is not found'
#        # return self.user.edit_one(id, args), 200, {'Content-Type': 'application/json'}
#    @jwt_required   
#    def delete(self, id):
#        qry_del = Users.query.get(id)
#        if qry_del is not None:
#            db.session.delete(qry_del)
#            db.session.commit()
#            return 'user with id = %d has been deleted' % id, 200, {'Content-Type': 'application/json'}
#        return {'status': 'ID_IS_NOT_FOUND'}, 404, {'Content-Type': 'application/json'}
#        
#    def patch(self):
#        return 'Not yet implemented', 501
#
#api.add_resource(UserResource, '', '/<int:id>')
##contoh kalau ke page itu sendiri :
##api.add_resource(UserResource, '', '/<int:id>')
#
#
##other example:
##bp_person = Blueprint('user', __name__, url_prefix='/user')
api.add_resource(RatingResource, '')
##example above is same with api.add_resource(UserResource, '/user', '/user/<int:id>') without url_prefix