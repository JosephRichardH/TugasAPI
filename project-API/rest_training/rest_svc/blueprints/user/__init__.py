import random, logging
from blueprints import db
from flask_restful import fields


class Users(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.String(50), nullable=True)
    client_id = db.Column(db.Integer)
    
    #unique=True kalau mau atribut nya unik, yang lain ga boleh ada yang sama

    response_field = {
        'id' : fields.Integer,
        'name' : fields.String,
        'age' : fields.Integer,
        'sex' : fields.String,
        'client_id' : fields.Integer
    }

    def __init__(self, id, name, age, sex, client_id):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex
        self.client_id = client_id

    def __repr__(self): #initiate table model
        return '<User %r>' % self.id #the __repr__ must have a string type as return
    
    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'age': self.age,
    #         'sex': self.sex,
    #         'client_id': self.client_id
    #     }

# class Users():
#     users = []
    
#     def __init__(self):
#         for i in range(15):
#             user = User()
#             user.id = i
#             user.name = "user ke %d" % (i)
#             user.age = random.randrange(17,60)
#             user.sex = random.choice(["male", "female"])
#             user.client_id = i
#             self.users.append(user.serialize())
#             # self.users.append(user.__dict__) bisa pake versi ini

#     def get_list(self):
#         return self.users
    
#     def add(self, str_serialized):
#         self.users.append(str_serialized)
#         return str_serialized

#     def get_by_id(self, id):
#         # for v in enumerate(self.users):
#         #     if v['id'] = id:
#         #         return v
#         # return None 
#         # or
#         # for v in self.users:
#         #     if v['id'] = id:
#         #         return v
#         for i in range(len(self.users)):
#             if (self.users[i]['id'] == id):
#                 return self.users[i]
#         return None
    
#     def get_by_name(self, name):
#         for i in range(len(self.users)):
#             if (self.users[i]['name'] == name):
#                 return self.users[i]
#         return None

#     def edit_one(self, id, str_serialized):
#         # for k, v in enumerate(self.users):
#         #     if int(v['id']) == int(id):
#         #         user = User()
#         #         user.id = id
#         #         user.name = name
#         #         user.age = age
#         #         user.sex = sex
#         #         self.users[k] = user.serialize()
#         #         return user
#         #     return None
#         for i in range(len(self.users)):
#             if self.users[i]['id'] == id:
#                 self.users[i]['id'] = str_serialized['id']
#                 self.users[i]['name'] = str_serialized['name']
#                 self.users[i]['age'] = str_serialized['age']
#                 self.users[i]['sex'] = str_serialized['sex']
#                 self.users[i]['client_id'] = str_serialized['client_id']
#                 return self.users[i]
#         return None
    
#     def delete_one(self, id):
#         for i in range(len(self.users)):
#             id_delt = self.users[i]['id']
#             if self.users[i]['id'] == id:
#                 del self.users[i]
#                 return 'user with id = %d has been deleted' % (id_delt)
#         return None 

