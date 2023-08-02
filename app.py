from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_login import login_required, LoginManager, current_user, login_user
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
import json
from utils import decorators as dc, dbconnect as db
from controllers import login_controller as loginctr
import mysql.connector
import hashlib 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Application set up
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}}) #allow any source
app.secret_key = os.environ.get("APP_SECRET_KEY")

#jwt configs
app.config["JWT_SECRET_KEY"]  = os.environ.get("APP_SECRET_KEY")
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  
jwt = JWTManager(app) 


# Database config
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER") 
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD") 
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB") 

# Intialize MySQL
isConnected, mysql = db.connect_to_mysql(app, mysql)
#test sql connection
if isConnected:
    print("Sql server connected")
else:
    print(mysql)
  
#limit brute force
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["60 per minute", "1 per second"],
    storage_uri="memory://",
    strategy="moving-window", # or "fixed-window"
)


@app.route('/') 
def home():
     return render_template('pages/home.html')


@app.route('/cpanel') 
@dc.login_required
def cpanel():
    return "Control panel"


@app.route('/login')
@dc.redirect_cpanel_if_loggedIn
def login():
    return render_template('pages/login.html')


@app.route('/statistics', methods = ['GET'])
@jwt_required()
def getStatistics():
    return jsonify({'message': "statistics gotten"})



@app.route('/logout',methods = ['GET'])
def logout(): 
    session.pop('loggedin', False)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('username', None) 
    return redirect(url_for('login'))


@app.route('/authenticate',methods = ['POST'])
@limiter.limit("50 per day")
def authenticate(): 
    try:
        jResponse = loginctr.login(request, mysql) 
        print(jResponse)
        response = jsonify(jResponse)
        response.set_cookie('access_token_cookie', value=jResponse['token'], httponly=True)  # Set HttpOnly cookie
        return response
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"loggedin": False, "message": "Service temporary unavailable"})