from flask import redirect, jsonify, url_for, session 
import hashlib
import json
from flask_jwt_extended import create_access_token
from flask_login import LoginManager, UserMixin, login_user, login_required
from models import user as u

 
def login(request, mysql):
    data_response = {}
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    password = password.encode()
    if email  and password: 
        password = hashlib.sha256(password).hexdigest() 
        print(password)

        cursor = mysql.cursor()
        query = "SELECT id, email, username FROM admins WHERE email = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchall()
        cursor.close()

        if len(result) > 0:
            user_id, user_email, username = result[0]
            session['loggedin'] = True
            session['user_id'] = user_id
            session['user_email'] = user_email
            session['username'] = username
            access_token = create_access_token(identity=user_id)
            data_response["loggedin"] = True
            data_response["token"] = access_token 
        else:
            data_response["loggedin"] = False
            data_response["token"] = ""
            data_response["message"] = "Wrong email or password!"
    else:
        data_response["loggedin"] = False
        data_response["token"] = ""
        data_response["message"] = "Please fill all fields in the form!!"
    
    #return 
    return data_response