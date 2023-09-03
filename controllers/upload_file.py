import hashlib
from utils import qrcode as qr  
from flask import session 
import uuid
import os

def saveFile(request, uploadFilePath):
    data_response = {}
    file = request.files['file']
    if file:
        uniqueId = str(uuid.uuid4())
        unique_filename = uniqueId + '.pdf'
        filepath = os.path.join(uploadFilePath, unique_filename)
        file.save(filepath)
        
        session['file_to_certify'] = filepath
        data_response["success"] = True 
        return data_response
    else:
        data_response["success"] = False
        data_response["message"] = "The file was not uploaded..."
        print("Noooo Fillllllllleeeeeeeee -----------")
        return data_response

        