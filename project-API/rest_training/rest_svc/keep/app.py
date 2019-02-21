from flask import Flask, request
import json 

app = Flask(__name__)

class Person():
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.name = None
        self.age = 0
        self.sex = None

@app.route('/')
def index():
    return '<h1>Hi, this is me</h1>'

@app.route('/name', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def name_controller():
    person = Person()
    if request.method == 'GET':
        pass
    elif request.method =='POST':
        pass
    elif request.method == 'PUT':
        data = request.get_json()
        person.name = data['name']
        person.age = data['age']
        person.sex = data['sex']
        return json.dumps(person.__dict__, 200, {'Content-Type': 'application/json'})
    elif request.method == 'DELETE':
        return 'Deleted', 200
    else:
        return 'Not yet implemented', 501
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)