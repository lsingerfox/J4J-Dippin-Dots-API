from flask import Flask, jsonify, request, session, redirect,json, url_for
from bson import json_util
from flask_jwt import current_identity
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length
from werkzeug.security import check_password_hash
from flask_login import logout_user
from j4jmd import db

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    

    def __str__(self):
        return "User(id=%s')" %self.id


    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    
    def login(self):
        form = LoginForm()
        email = request.json['email']
        user = db.admin.find_one({"email": email})
        print(form.password.data)
        print(user['password'])  
        if user and check_password_hash(user['password'], form.password.data):
            return jsonify({ "msg": "Welcome Back, " + json.loads(json_util.dumps(user["name"])) + "!"}), 200
        else:
            return jsonify({ "error": "Invalid email or password"}), 401


    def protected():
        return '%s' % current_identity
    

    def signout(self):
        logout_user()
        return redirect(url_for('home'))