from flask import Flask, request, jsonify, Response
from flask_jwt_extended.utils import create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from bson import json_util
from bson.objectid import ObjectId
from pymongo import MongoClient
from flask_pymongo import PyMongo
import gridfs
import jwt
import datetime
import hashlib
import json
import os

from flask_jwt_extended import create_access_token, JWTManager


from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from werkzeug.wrappers import response

app = Flask(__name__)

app.secret_key = 'H0verM@g1c'

jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'H0verM@g1c'
app.config["MONGO_URI"] = "mongodb+srv://lrsinger:Und3rt%40lel0ver@dippin-dots-j4j-dont-te.xwqye.mongodb.net/Dippin-Dots-J4J-DONT-TERMINATE?retryWrites=true&w=majority"

MongoClient = PyMongo(app)
db = MongoClient.db


#Creating New User
# @app.route('/api/v1/users', methods=['POST'])
# def create_user():
#     firstName = request.json['firstName']
#     lastName = request.json['lastName']
#     companyName = request.json['companyName']
#     username = request.json['username']
#     password = request.json['password']
#     streetAddress = request.json['streetAddress']
#     city = request.json['city']
#     state = request.json['state']
#     zip = request.json['zip']
#     phone = request.json['phone']
#     email = request.json['email']
#     iceCreamPrice = request.json['iceCreamPrice']
#     spoonPrice = request.json['spoonPrice']
#     admin = request.json['admin']
#     active = request.json['active']
    

#     if username and email and password:
#         hashed_password = generate_password_hash(password)
#         id = db.users.insert(
#             {'firstName': firstName, 
#             'lastName': lastName, 
#             'companyName': companyName,
#             'username': username, 
#             'password': hashed_password, 
#             'streetAddress': streetAddress, 
#             'city': city, 
#             'state': state, 
#             'zip': zip, 
#             'phone': phone,
#             'email': email,
#             'iceCreamPrice': iceCreamPrice,
#             'spoonPrice': spoonPrice,
#             'admin': admin,
#             'active': active
#             }
#         )
#         response = jsonify({
#             '_id': str(id),
#             'firstName': firstName, 
#             'lastName': lastName, 
#             'companyName': companyName,
#             'username': username,
#             'password': password,
#             'streetAddress': streetAddress, 
#             'city': city, 
#             'state': state, 
#             'zip': zip, 
#             'phone': phone,
#             'email': email,
#             'iceCreamPrice': iceCreamPrice,
#             'spoonPrice': spoonPrice,
#             'admin': admin,
#             'active': active
#         })

#Grab User(s)
@app.route('/users', methods=['GET'])
def get_users():
    print(id)
    users = db.users.find()
    response = json_util.dumps(users)
    return Response(response, mimetype="application/json")


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    print(id)
    user = db.users.find_one({id: ObjectId(id), })
    response = json_util.dumps(user)
    return Response(response, mimetype="application/json")


@app.route('/token', methods=['POST'])
def create_token():
    username=request.json["username"]
    password=request.json["password"]
    user = db.users.find_one({username:username, password:password })
    if user is None:
        return jsonify({"msg": "Username not found"}),401
    else:
        access_token=create_access_token(identity=user.id)
        return jsonify({"token": access_token})


#Delete User
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db.users.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User' + id + 'Deleted Successfully'})
    response.status_code = 200
    return response


#Update User
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
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
    if username and email and password and id:
        hashed_password = generate_password_hash(password)
        db.users.update_one(
            {'id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {'firstName': firstName, 
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
            'active': active}})
        response = jsonify({'message': 'User' + id + 'Updated Successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()

#Add Product
@app.route('/api/v1/products', methods=['POST'])
def add_product():
    productName = request.json['productName']
    price = request.json['price']
    category = request.json['category']
    active = request.json['active']
    if productName and price and category:
        db.products.insert(
            {
                'productName': productName,
                'price': price,
                'category': category,
                'image': image(""),
                'active': active
            }
        )
        response = jsonify({
            '_id': str(id),
            'productName': productName,
            'price': price,
            'category': category,
            'image': image(""),
            'active': active
        })
        response.status_code = 200
        return response
    else:
        return not_found()

#Get Product(s)
@app.route('/products', methods=['GET'])
def products():
    print(id)
    products = db.products.find()
    response = json_util.dumps(products)
    return Response(response, mimetype="application/json")


@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    print(id)
    product = db.products.find_one({id: ObjectId(id), })
    response = json_util.dumps(product)
    return Response(response, mimetype="application/json")

#Delete Product
@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    db.products.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Product' + id + 'Deleted Successfully'})
    response.status_code = 200
    return response


#Update Product
@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    productName = request.json['productName']
    price = request.json['price']
    category = request.json['category']
    active = request.json['active']
    if productName and category and id:
        db.products.update_one(
            {'id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': { 
            'productName': productName,
            'price': price,
            'category': category,
            'image': image(""),
            'active': active}})
        response = jsonify({'message': 'Product' + id + 'Updated Successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()

#Add Event
@app.route('/events', methods=['POST'])
def add_event():
    eventName = request.json['eventName']
    date = request.json['date']
    time = request.json['time']
    description = request.json['description']
    if eventName and date and time:
        db.events.insert(
            {
                'eventName': eventName,
                'date': date,
                'time': time,
                'description': description
            }
        )
        response = jsonify({
            '_id': str(id),
            'eventName': eventName,
            'date': date,
            'time': time,
            'description': description
        })
        response.status_code = 200
        return response
    else:
        return not_found()

#Get Event(s)
@app.route('/events', methods=['GET'])
def get_events():
    print(id)
    events = db.events.find()
    response = json_util.dumps(events)
    return Response(response, mimetype="application/json")


@app.route('/events/<id>', methods=['GET'])
def get_event(id):
    print(id)
    event = db.events.find_one({id: ObjectId(id), })
    response = json_util.dumps(event)
    return Response(response, mimetype="application/json")

#Delete Event
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    db.events.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Event' + id + 'Deleted Successfully'})
    response.status_code = 200
    return response


#Update Event
@app.route('/events/<id>', methods=['PUT'])
def update_event(id):
    eventName = request.json['eventName']
    date = request.json['date']
    time = request.json['time']
    description = request.json['description']
    if eventName and date and time and id:
        db.events.update_one(
            {'id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)}, {'$set': {
            'eventName': eventName,
            'date': date,
            'time': time,
            'description': description}})
        response = jsonify({'message': 'Event' + id + 'Updated Successfully'})
        response.status_code = 200
        return response
    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(debug=True)