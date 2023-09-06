from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_login import login_required, LoginManager, current_user, login_user
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
import os
from web3 import Web3
import json
from utils import decorators as dc, dbconnect as db, fileUtils as fu
from controllers import login_controller as loginctr, requests_controller as reqCtrl, upload_file as upFile, document_controller as dCtrl
import mysql.connector
import hashlib 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import openai

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
UPLOAD_FILE_PATH = os.environ.get("DOCUMENTS_UPLOAD_FILE_PATH")

#blockchain configs
rpc_server = os.environ.get("RPC_SERVER")
abi_file_path = os.environ.get("CONTRACT_ABI_FILE_PATH")
user_address = os.environ.get("DEFAULT_USER_ADRESS")

#openai configs 
FINE_TUNED_MODEL = os.environ.get("OPENAI_FINE_TUNED_MODEL_ID")
openai.organization = os.environ.get("OPENAI_ORG_ID")
openai.api_key = os.environ.get("OPENAI_API_KEY")

IPFS_API_SERVER = os.environ.get("IPFS_API_SERVER")

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


# init web3 and default account
web3 = Web3(Web3.HTTPProvider(rpc_server))
web3.eth.default_account = user_address 
abi, contract_address = fu.getAbiAndContractAddr(abi_file_path)

# Create the contract instance
contract = web3.eth.contract(address=contract_address, abi=abi)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('pages/404.html'), 404


@app.route('/') 
def home():
    return render_template('pages/home.html')

@app.route('/request') 
def requestDocument():
    facultyies = reqCtrl.faculty(mysql) 
    departs = reqCtrl.departments(mysql, "1") 
    orientations = reqCtrl.orientations(mysql, "1") 
    docs = reqCtrl.documents(mysql) 
    return render_template('pages/request-page.html', facs = facultyies, depts = departs, orients = orientations, docs = docs)

@app.route('/pay') 
def payforDocument():
    req = reqCtrl.getCurrentRequest(mysql) 
    price = reqCtrl.getPrice(mysql, req["document"]) 
    return render_template('pages/request-payment-page.html', doc = req["document"] + " / "+ req["promotion"], year = req["year"], price = price)



@app.route('/success-pay') 
def successPay():
    return render_template('pages/request-success.html')

@app.route('/verify') 
def verifyDocument():
    return render_template('pages/verify-page.html')


@app.route('/cpanel') 
@dc.login_required
def cpanel():
    username = session.get('username')
    if username is not None:
        return render_template('pages/dashboard.html', username=username.upper())
    else:
        return render_template('pages/dashboard.html')


@app.route('/cpanel/certificates') 
@dc.login_required
def certificates():
    username = session.get('username')
    if username is not None:
        return render_template('pages/dashboard.html', username=username.upper())
    else:
        return render_template('pages/dashboard.html')


@app.route('/cpanel/requests') 
@dc.login_required
def requests():
    username = session.get('username')
    if username is not None:
        return render_template('pages/dash-requests.html', username=username.upper())
    else:
        return render_template('pages/dash-requests.html')


@app.route('/cpanel/view-request/<id>')
def view_request(id):
    username = session.get('username')
    if username is not None:
        return render_template('pages/dash-view-request.html', username=username.upper())
    else:
        return render_template('pages/dash-view-request.html')

        
@app.route('/cpanel/verifications') 
@dc.login_required
def verifications():
    username = session.get('username')
    if username is not None:
        return render_template('pages/dashboard.html', username=username.upper())
    else:
        return render_template('pages/dashboard.html')

@app.route('/cpanel/settings') 
@dc.login_required
def settings():
    username = session.get('username')
    if username is not None:
        return render_template('pages/dashboard.html', username=username.upper())
    else:
        return render_template('pages/dashboard.html')
    


@app.route('/login')
@dc.redirect_cpanel_if_loggedIn
def login():
    return render_template('pages/login.html')


@app.route('/statistics', methods = ['GET'])
@dc.login_required
def getStatistics():
    return jsonify({'message': "statistics gotten"})

@app.route('/logout',methods = ['GET'])
def logout(): 
    session.pop('loggedin', False)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('username', None) 
    return redirect(url_for('login'))

##### Jquery Requests ##############
@app.route('/doc-certify-now', methods=['POST'])
def certifyNow():
     certId = request.json.get('certId', None)
     rep = dCtrl.certify(request, UPLOAD_FILE_PATH, openai, IPFS_API_SERVER, contract, user_address)

     return jsonify(rep)

@app.route('/fileupload', methods=['POST']) 
def uploadDocument():
    try:
        if "loggedin" in session and session['loggedin'] == True:
            rep = upFile.saveFile(request, UPLOAD_FILE_PATH) 
            return jsonify(rep)
        else:
            return "bad request", 401
    except Exception as e:
        print("An error occurred:", e)
        return "bad request", 401


@app.route('/save-request', methods = ['POST'])
def saveRequest():
    try:  
        return jsonify(reqCtrl.addRequest(request, mysql))
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"success": False, "message": "Service temporary unavailable"})

@app.route('/save-paiement', methods=['POST'])
def savePaiement():
    try:  
        return jsonify(reqCtrl.addPaiement(request, mysql))
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"success": False, "message": "Service temporary unavailable"})

@app.route('/authenticate',methods = ['POST'])
@limiter.limit("50 per day")
def authenticate(): 
    try:
        jResponse = loginctr.login(request, mysql)  
        response = jsonify(jResponse)
        response.set_cookie('access_token_cookie', value=jResponse['token'], httponly=True)  # Set HttpOnly cookie
        return response
    except Exception as e:
        print("An error occurred:", e)
        return jsonify({"loggedin": False, "message": "Service temporary unavailable"})