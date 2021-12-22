from flask import Flask, request, jsonify,json,session, redirect, render_template, url_for
from pymongo import MongoClient
# from flask_jwt import jwt_required, current_identity
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from wtforms.validators import InputRequired, Length
# from werkzeug.security import check_password_hash
from functools import wraps
# from flask_login import login_required, logout_user, current_user
import os
from bson import json_util

# class User():
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password
    

#     def __str__(self):
#         return "User(id=%s')" %self.id
    

#     def start_session(self,user):
#         del user['password']
#         session['logged_in'] = True
#         session['user'] = user
#         return jsonify(user), 200
    


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = 'H0verM4gic'
app.config['MONGO_URI'] = ("mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
s = MongoClient ("mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = s.db


# class LoginForm(FlaskForm):
#     email = StringField('Email', validators=[InputRequired(), Length(min=8, max=100)])
#     password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])


# @app.route("/user/login/", methods = ["POST"])
# def login():
#     form = LoginForm()
#     email = request.json['email']
#     user = db.admin.find_one({"email": email})
#     print(form.password.data)
#     print(user['password'])  
#     if user and check_password_hash(user['password'], form.password.data):
#         return jsonify({ "msg": "Welcome Back, " + json.loads(json_util.dumps(user["name"])) + "!"}), 200
#     else:
#         return jsonify({ "error": "Invalid email or password"}), 401


# @app.route('/dashboard/')
# @login_required
# def dashboard():
#     return render_template('dashboard.html', name=current_user.name)


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('home'))


# @app.route('/protected')
# @jwt_required()
# def protected():
#     return '%s' % current_identity

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return jsonify('Back to Home Page')
    
    return wrap


import routes

@app.route('/')
def home():
    return jsonify('Home Page')


@app.route('/dashboard/')
@login_required
def dashboard():
    return jsonify('Welcome to Dashboard')

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