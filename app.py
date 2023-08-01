from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_login import login_required, LoginManager, current_user, login_user
from flask_jwt_extended import JWTManager
import os
import json
from utils import decorators as dc, dbconnect as db
from controllers import login_controller as loginctr
import mysql.connector
import hashlib
 

# Application set up
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}) #allow any source
app.secret_key = os.environ.get("APP_SECRET_KEY")

#jwt manager
app.config["JWT_SECRET_KEY"]  = os.environ.get("APP_SECRET_KEY")
jwt = JWTManager(app)


# Database config
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER") 
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD") 
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB") 

# Intialize MySQL
isConnected, mysql = db.connect_to_mysql(app, mysql)

if isConnected:
    print("Sql server connected")
else:
    print(mysql)

# Login Management
login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'


@app.route('/') 
def home():
    return "hello"


@app.route('/cpanel') 
@dc.login_required
def cpanel():
    return "Control panel"


@app.route('/login')
@dc.redirect_cpanel_if_loggedIn
def login():
    return render_template('pages/login.html')


@app.route('/logout',methods = ['GET'])
def logout():
    session.pop('loggedin', False)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('username', None) 


@app.route('/authenticate',methods = ['POST'])
def authenticate(): 
    try:
        response = loginctr.login(request, mysql) 
        print(response)
        return jsonify(response)
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"loggedin": False, "message": "Service temporary unavailable"})