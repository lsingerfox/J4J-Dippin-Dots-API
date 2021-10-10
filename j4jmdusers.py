from flask import Flask, request, jsonify, Response
from flask_jwt import JWT, jwt_required, current_identity
from pymongo import MongoClient
from flask_pymongo import PyMongo
from flask_jwt_extended.utils import create_access_token
import pymongo
from werkzeug.security import safe_str_cmp, generate_password_hash

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    

    def __str__(self):
        return "User(id=%s')" % self.id


users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authentication(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'H0verm@gic'
app.config['MONGO_URI'] = "mongodb+srv://lrsinger:Und3rt%40lel0ver@dippin-dots-j4j-dont-te.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

jwt = JWT(app, authentication, identity)

MongoClient = PyMongo(app)
db = MongoClient.db

#Creating New User
@app.route('/api/v1/users', methods=['POST'])
def create_user():
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    companyName = request.json['companyName']
    username = request.json['username']
    password = request.json['password']
    streetAddress = request.json['streetAddress']
    city = request.json['city']
    state = request.json['state']
    zip = request.json['zip']
    phone = request.json['phone']
    email = request.json['email']
    iceCreamPrice = request.json['iceCreamPrice']
    spoonPrice = request.json['spoonPrice']
    admin = request.json['admin']
    active = request.json['active']
    

    if username and email and password:
        hashed_password = generate_password_hash(password)
        id = db.users.insert(
            {'firstName': firstName, 
            'lastName': lastName, 
            'companyName': companyName,
            'username': username, 
            'password': hashed_password, 
            'streetAddress': streetAddress, 
            'city': city, 
            'state': state, 
            'zip': zip, 
            'phone': phone,
            'email': email,
            'iceCreamPrice': iceCreamPrice,
            'spoonPrice': spoonPrice,
            'admin': admin,
            'active': active
            }
        )
        response = jsonify({
            '_id': str(id),
            'firstName': firstName, 
            'lastName': lastName, 
            'companyName': companyName,
            'username': username,
            'password': password,
            'streetAddress': streetAddress, 
            'city': city, 
            'state': state, 
            'zip': zip, 
            'phone': phone,
            'email': email,
            'iceCreamPrice': iceCreamPrice,
            'spoonPrice': spoonPrice,
            'admin': admin,
            'active': active
        })


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


if __name__ == '__main__':
    app.run()