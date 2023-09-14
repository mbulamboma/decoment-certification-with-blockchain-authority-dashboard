import uuid
import os
import hashlib
from flask import session
from utils import qrcode as qr
from utils import ipfs as fs
from utils import eth 
from utils import prompt as ai 
import PyPDF2
from controllers import requests_controller as reqCtrl
import time
import requests as rq
import csv
def checkDocument(request, contract, user_address):
    data_response = {} 
    hashText = request.json.get('hashtext', None)
    if eth.checkIfExist(hashText, contract, user_address):
        datas =  eth.getRecordFromBlockChain(hashText, contract, user_address)  
        a = "<h6>This document has been certified by us, please view the integral electronic version of that.</h6><br />"
        b = f"<a href='http://127.0.0.1:8080/ipfs/{datas['fileHash']}'>Click here to see the integral version</a>"
        data_response["message"] = a + b

    else: 
        data_response["message"] = "This document is not authentic, please contact the issuer authority for better assistance"

    return data_response
          


def certify(mysql, request, uploadFilePath, openai, ipfsBaseUrl, contract, user_address):
    start_time = time.time()
    data_response = {} 
    #requestId = request.json.get('certId', None)
    #response = rq.get("https://google.com")  # Make the HTTP request
    #end_time = time.time()
    #request_run_time = end_time - start_time
    #response_size_bytes = len(response.content)
    #network_bandwidth = response_size_bytes / request_run_time
    network_bandwidth = 0
    if 'file_to_certify' in session and session['file_to_certify'] != None: 
        uniqueId = str(uuid.uuid4())
        filepath = session['file_to_certify'] 
        
        # read the file content
        with open(filepath, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            file_content = ''
            for page_num in range(len(pdf_reader.pages)):
                # Get the text content of the current page
                page = pdf_reader.pages[page_num]
                file_content += page.extract_text() 
            f.close()
 
        #rowhashText = ai.getDocumentInfos(file_content, openai)
        rowhashText = '{"document_title":"studenttranscript","student_name":"yediddamvuladd","academic_year":"2021–2022","option":"genieinformatique","year_of_study":"deuxiemeepreuveingenieurcivil"}'
        print(rowhashText)
        hashText = hashlib.sha256(rowhashText.encode('utf-8')).hexdigest()
        if eth.checkIfExist(hashText, contract, user_address): 
            datas =  eth.getRecordFromBlockChain(hashText, contract, user_address) 
            data_response["success"] = True
            data_response["message"] = "The document is successfully certified."
            data_response["ipfs-url"] = f"http://127.0.0.1:8080/ipfs/{datas['fileHash']}" 

            end_time2 = time.time()
            final_run_time = end_time2 - start_time
            print(f"Request Type: Second time")
            print(f"Request Size: 0 bytes")
            print(f"Request Run Time: {final_run_time:.2f} seconds") 
            print(f"Network Bandwidth: 0 bytes/second")
            #save the document hash
            #save the document hash
            #print("222222----------------- "+datas['fileHash'])
            #reqCtrl.updateRequest(mysql, datas['fileHash'], requestId, hashText) 
            with open('requests.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["yes", f"{final_run_time:.2f}", "0"])
                csvfile.close()
            return data_response
        
        pathOfTheCertifiedDocument = os.path.join(uploadFilePath, uniqueId+"-certified.pdf")
        easyUrlToVerifyTheDocument = f"http://localhost:5000/verify/{hashText}"
        qr.gen_certified_document(hashText, filepath, pathOfTheCertifiedDocument, easyUrlToVerifyTheDocument, uploadFilePath)

        ipfsIDHash = fs.uploadFile(pathOfTheCertifiedDocument, ipfsBaseUrl)
        eth.saveRecordInBlockChain(ipfsIDHash, hashText,  contract, user_address)
        
        data_response["success"] = True
        data_response["message"] = "The document is successfully certified."
        data_response["ipfs-url"] = f"http://127.0.0.1:8080/ipfs/{ipfsIDHash}"
        end_time2 = time.time()
        final_run_time = end_time2 - start_time
        
        print(f"Request Type: First time")
        print(f"Request Size: 0 bytes")
        print(f"Request Run Time: {final_run_time:.2f} seconds") 
        print(f"Network Bandwidth: 0 bytes/second")
        #save the document hash
        #print("11111----------------- "+ipfsHash)
        #reqCtrl.updateRequest(mysql, ipfsIDHash, requestId, hashText) 
        with open('requests.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["no", f"{final_run_time:.2f}", f"{network_bandwidth:.2f}"])
            csvfile.close()
        session['file_to_certify'] =  None
        return data_response 
    else:
        data_response["success"] = False
        data_response["message"] = "The file was not uploaded..."
        return data_response

        