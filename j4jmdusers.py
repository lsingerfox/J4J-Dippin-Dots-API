from bson.objectid import ObjectId
from flask import Flask, request, jsonify, session,redirect,url_for
from flask.templating import render_template
from flask_jwt import JWT, jwt_required, current_identity
from pymongo import MongoClient
import dnspython3
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, BooleanField, IntegerField,SubmitField
from wtforms.validators import InputRequired, Length
import certifi
from werkzeug.security import check_password_hash, safe_str_cmp, generate_password_hash
from flask_login import login_required, logout_user, current_user

class User(object):
    def __init__(self, _id, email, password):
        self._id = _id
        self.email = email
        self.password = password

    
    def __str__(self):
        return "User(id=%s')" % self.id

    def authentication(email, password):
        user = db.users.get(email, None)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return user


    def identity(payload):
        _id = payload['identity']
        return db.users.get(_id, None)

    
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'H0verm@gic'
app.config['MONGO_URI'] = "mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/database?retryWrites=true&w=majority"

jwt = JWT(app, User.authentication, User.identity)

s = MongoClient("mongodb+srv://lrsinger:Und3rt4lel0ver2015@database.xwqye.mongodb.net/database?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = s.db


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(min=8, max=100)])
    firstName = StringField('First Name', validators=[InputRequired(), Length(min=2, max=100)])
    lastName = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=100)])
    companyName = StringField('Company Name', validators=[Length(min=0, max=100)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    streetAddress = StringField('Street Address', validators=[InputRequired(), Length(min=4, max=100)])
    city = StringField('City', validators=[InputRequired(), Length(min=3, max=60)])
    state = StringField('State', validators=[InputRequired(), Length(2)])
    zip = IntegerField('Zip', validators=[InputRequired()])
    phone = IntegerField('Phone', validators=[InputRequired()])
    admin = BooleanField(False)
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('home.html')



@app.route('/signup', methods=['POST'])
def signup():
    form = RegisterForm()

    form.password.data = generate_password_hash(form.password.data)

    if db.users.find_one({ "email": form.email.data }):
        return jsonify({ "error": "Email address already in use "}), 400

    if form.validate_on_submit() and db.users.insert_one(form):
        return jsonify({ "msg": "Welcome to the world of Dippin' Dots by Jump 4 Joy"}), 200

    print(form.errors)

    return jsonify({ "error": "Signup failed" }), 400

@app.route('/login/', methods=['POST'])
def login():
    form = LoginForm()
    email= request.json['email']
    user = db.users.find_one({"email": email})
    print(form.password.data)
    print(user['password'])
    if user and check_password_hash(user['password'],form.password.data):
        #return render_template('dashboard.html')
        return jsonify ({ "msg": "Welcome in!" }), 200
    else:
        print('Invalid email or password')
        return jsonify ({ "error" : "Invalid email or password" }), 401

    


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.firstName)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


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

if __name__ == '__main__':
    app.run()