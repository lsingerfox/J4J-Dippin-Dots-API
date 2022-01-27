from email.mime import image
import imp
from flask import Flask, request, jsonify,json,session, redirect, render_template, url_for
from pymongo import MongoClient, database
from flask_jwt import jwt_required, current_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash
from flask_login import login_required, logout_user, current_user
import base64
import os
from bson import json_util
from flask_cors import CORS

class User():
    def __init__(self, name, email, phone, password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
    

    def __str__(self):
        return "User(id=%s')" %self.id
    

    def start_session(self,user):
        del user['password']
        session['LOGGED_IN'] = True
        session['user'] = user
        return jsonify(user), 200
    


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'H0verM4gic'
app.config['MONGO_URI'] = ("mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
s = MongoClient ("mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = s.db
CORS(app)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])



class UserSession():
    @app.route("/", methods = ["POST","GET"])
    def home():
        return "j4j API"

    @app.route("/user/login", methods = ["POST"])
    def login():
        form = LoginForm()
        email = request.json['email']
        user = db.admin.find_one({"email": email})
        print(form.password.data)
        print(user['password'])  
        if user and check_password_hash(user['password'], form.password.data):
            return ({"data": json.loads(json_util.dumps(user))})
        else:
            return jsonify({ "error": "Invalid email or password"}), 401


    @app.route('/dashboard/', methods = ["POST", "GET"])
    @login_required
    def dashboard():
        user = User.start_session()
        return (user)


    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home')), 200


    @app.route('/protected')
    @jwt_required()
    def protected():
        return '%s' % current_identity


    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'message': 'Resource Not Found: ' + request.url,
            'status': 404
        }
        response = jsonify(message)
        response.status_code = 404
        return response


class Products():
    @app.route("/products", methods = ["POST"])
    def products():
        title = request.json['title']
        product = db.products.find({"title": title})
        return ({"data": json.loads(json_util.dumps(product))}), 200
    

    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'message': 'Resource Not Found: ' + request.url,
            'status': 404
        }
        response = jsonify(message)
        response.status_code = 404
        return response


if __name__ == "__main__":
    app.run(debug=True)