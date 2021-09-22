from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from bson import json_util
from bson.objectid import ObjectId
import pymongo
import gridfs
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import datetime
import hashlib
import json
import os


from werkzeug.security import generate_password_hash, check_password_hash, safe_str_cmp
from werkzeug.wrappers import response

app = Flask(__name__)

app.secret_key = 'H0verM@g1c'

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'H0verM@g1c'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

client = pymongo.MongoClient("mongodb+srv://lrsinger:Und3rt%40lel0ver2015@dippin-dots-j4j.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["mydatabase"]
users_collection = db["users"]
products_collection = db["products"]
events_collection = db["events"]

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

def image():
    fs = gridfs.GridFS(db)
    file = image("")
    with open(file, 'rb') as f:
        contents = f.read()
    fs.put(contents, filename = 'file')


#Creating New User
@app.route('/api/v1/users', methods=['POST'])
def register():
    new_user = request.get_json()
    new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    doc = users_collection.find_one({"username": new_user["username"]})
    if not doc:
        users_collection.insert_one(new_user)
        return jsonify({'msg': 'User created sccessfully'}), 201
    else:
        return jsonify({'msg': 'Username already exists'}), 409

#User Login
@app.route('/api/v1/login', methods=["POST"])
def login():
    login_details = request.get_json()
    user_from_db = users_collection.find_one({'username': login_details['username']})

    if user_from_db:
        encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
        if encrpted_password == user_from_db['password']:
            access_token = create_access_token(identity=user_from_db['username'])
            return jsonify(access_token=access_token), 200

    return jsonify({'msg': 'The username or password is incorrect'}), 401

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
@app.route('/products', methods=['POST'])
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

#Get Product(s)
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

#Delete Product
@app.route('/events/<id>', methods=['DELETE'])
def delete_event(id):
    db.events.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Event' + id + 'Deleted Successfully'})
    response.status_code = 200
    return response


#Update Product
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


if __name__ == '__main__':
    app.run(debug=True)