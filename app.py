from flask import Flask, request, jsonify,json,session, redirect, render_template, url_for
from pymongo import MongoClient, database
from flask_jwt import jwt_required, current_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash
from flask_login import login_required, logout_user, LoginManager
import os
from bson import json_util
from flask_cors import CORS,cross_origin

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
login = LoginManager(app)


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


    @app.route('/logout', methods = ["POST"])

    def logout():
        message = {
            'message': 'Logout Successful!',
            'status': 200
        }
        response = jsonify(message)
     
        return response


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
    @app.route("/products", methods = ["GET"])
    @cross_origin(supports_credentials=True)
    def products():

        product = db.products.find({})
        return ({"data": json.loads(json_util.dumps(product))})
    

    @app.errorhandler(404)
    def not_found(error=None):
        message = {
            'message': 'Resource Not Found: ' + request.url,
            'status': 404
        }
        response = jsonify(message)
        response.status_code = 404
        return response


class ContactForm(FlaskForm):
    fullName = StringField("Full Name", validators=[InputRequired()])
    companyName = StringField("Company Name")
    email = StringField("Email", validators = [InputRequired()])
    phone = IntegerField("Phone Number", validators=[InputRequired(), Length(min=8)])
    subject = StringField("Subject", validators=[InputRequired()])
    message = TextAreaField ("Message", validators = [InputRequired()])
    submit = SubmitField("Send")


class Contact():
    @app.route('/contact', methods=["POST"])
    def contact():
        form = ContactForm()
        if ({form.fullName == True}, {form.email == True}):
            return jsonify({"msg":"Thank you for your message! You should receive a response within 24 to 48 hours."}), 200
        else:
            return jsonify({ "error": "Please fill out the necessary items on the form"}), 401
    

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