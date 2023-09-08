from flask import redirect, jsonify, url_for, session 
import hashlib
import json
from flask_jwt_extended import create_access_token
from flask_login import LoginManager, UserMixin, login_user, login_required
from models import user as u


def getTop10Request(mysql):
    cursor = mysql.cursor()
    query = "SELECT * FROM requests LIMIT 50"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def getRequestById(mysql, id):
    cursor = mysql.cursor()
    query = "SELECT * FROM requests WHERE id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]

def getPaymentInfos(mysql, id):
    cursor = mysql.cursor()
    query = "SELECT * FROM payments WHERE req_id = %s"
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    cursor.close()
    return result[0]


def faculty(mysql):
    cursor = mysql.cursor()
    query = "SELECT * FROM facultes"
    cursor.execute(query)
    result = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return result


def departments(mysql, facId):
    cursor = mysql.cursor()
    query = "SELECT * FROM departements  WHERE fac_id = %s "
    cursor.execute(query, (facId, ))
    result = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return result

def orientations(mysql, deptId):
    cursor = mysql.cursor()
    query = "SELECT * FROM orientations "
    cursor.execute(query)
    result = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return result


def documents(mysql):
    cursor = mysql.cursor()
    query = "SELECT * FROM documents "
    cursor.execute(query)
    result = [row[1] for row in cursor.fetchall()]
    cursor.close()
    return result


def getPrice(mysql, document):
    cursor = mysql.cursor()
    query = "SELECT price FROM documents WHERE label = %s "
    cursor.execute(query, (document,))
    result = cursor.fetchall()
    cursor.close()
    if len(result) > 0:
        return result[0][0]
    else:
        return 0


def getCurrentRequest(mysql):
    last_request_id = session['lastRequestId']
    cursor = mysql.cursor()
    query = "SELECT * FROM requests WHERE id = %s "
    cursor.execute(query, (last_request_id,))
    result = cursor.fetchall()
    cursor.close()
    
    if len(result) > 0:
        return { 
            "document" : result[0][3],
            "promotion" : result[0][7],
            "year" : result[0][8],
        } 
    else: 
        return {
            "id" : "",
            "document" : "",
            "promotion" : "",
        }

def addPaiement(request, mysql): 
    data_response = {}
    req_id = session['lastRequestId']
    paid = True
    email = request.json.get('email', None)
    phone = request.json.get('phone', None) 

    if email is None or phone is None or 'lastRequestId' not in session:
        data_response["success"] = False
        data_response["message"] = "Please, some fields are empty"
        if 'lastRequestId' not in session:
            data_response["message"] = "Please, Restart from step 1"
            data_response["next"] = "/home"
        return dashboard
    
    cursor = mysql.cursor()
    query = "INSERT INTO payments (id, req_id, email, phone, paid, created_at) VALUES (NULL, %s, %s, %s, %s, current_timestamp());"
    cursor.execute(query, (req_id, email, phone, paid)) 
    mysql.commit()
    inserted_id = cursor.lastrowid
    cursor.close()
    session['lastRequestId'] = None

    data_response["success"] = True
    data_response["message"] = "Request has been successfully saved..."
    data_response["next"] = "/success-pay"
    #return 
    return data_response


def updateRequest(mysql, ipfsHash, req_id, docHash):
    cursor = mysql.cursor()
    query = "UPDATE requests SET ipfs_hash = %s, doc_hash = %s WHERE id = %s;"
    cursor.execute(query, (ipfsHash, docHash, req_id)) 
    mysql.commit()
    cursor.close()



def addRequest(request, mysql): 
    data_response = {}
    fullname = request.json.get('fullname', None)
    studentId = request.json.get('studentId', None)
    faculty = request.json.get('faculty', None)
    document = request.json.get('document', None)
    department = request.json.get('department', None)
    orientation = request.json.get('orientation', None)
    promotion = request.json.get('promotion', None)
    year = request.json.get('year', None)

    if fullname is None or studentId is None or faculty is None or document is None or department is None or orientation is None or year is None:
        data_response["success"] = False
        data_response["message"] = "Please, some fileds are empty"
        return dashboard
    
    
    cursor = mysql.cursor()
    ## As long as he did not pay update the already inserted ID
    if 'lastRequestId' not in session:
        query = "INSERT INTO requests (id, full_name, student_id, document_id, faculty, department, orientation, academic_year, promotion, requested_at) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, current_timestamp());"
        cursor.execute(query, (fullname, studentId, document, faculty, department, orientation, year, promotion)) 
        mysql.commit()
        inserted_id = cursor.lastrowid
        cursor.close()
        session['lastRequestId'] = inserted_id
    else:
        last_request_id = session['lastRequestId']
        query = "UPDATE requests SET full_name = %s, student_id = %s, document_id = %s, faculty = %s, department = %s, orientation = %s, academic_year = %s, promotion = %s WHERE id = %s;"
        cursor.execute(query, (fullname, studentId, document, faculty, department, orientation, year, promotion, last_request_id)) 
        mysql.commit()
        cursor.close()


    data_response["success"] = True
    data_response["message"] = "Request has been successfully saved..."
    data_response["next"] = "/pay"
    #return 
    return data_response