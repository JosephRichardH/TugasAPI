from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
from time import strftime
import json, logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand 
from blueprints import *
from flask_script import Manager
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)
## initiate flask-restful instance
api = Api(app, catch_all_404s=True)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@0.0.0.0:3306/rest_training'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) #bestpractice expiry is 1 hour

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return identity


db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@app.after_request
def after_request(response):
    if request.method == 'GET':
        app.logger.warning("REQUEST LOG\t%s\t%s", request.method, json.dumps({'request': request.args.to_dict(), 'response': json.loads(response.data.decode('utf-8')) }))
    else:
        app.logger.warning ("REQUEST LOG\t%s\t%s",  request.method, json.dumps({'request': request.get_json(), 'response': json.loads(response.data.decode('utf-8')) }))
    return response

#call blueprint

from blueprints.semua.resources import bp_semua
from blueprints.harga.resources import bp_harga
from blueprints.daerah.resources import bp_daerah




app.register_blueprint(bp_semua, url_prefix='/semua')
app.register_blueprint(bp_harga, url_prefix='/harga')
app.register_blueprint(bp_daerah, url_prefix='/daerah')

db.create_all()

