from flask import Flask
from j4jmd import app
from models import User
from flask_login import login_required
from flask_jwt import jwt_required

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()


@app.route('/protected')
@jwt_required()
def protected():
    return User().protected()


@app.route('/user/signout')
@login_required
def signout():
    return User().signout()