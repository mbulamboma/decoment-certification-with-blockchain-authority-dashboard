
import hashlib
from utils import qrcode as qr
from utils import ipfs as fs
from utils import eth 
from utils import prompt as ai 

def certify(request, uploadFilePath, openai, ipfsBaseUrl):
    data_response = {}
    file = request.files['myFile']
    if file:
        uniqueId = str(uuid.uuid4())
        unique_filename = uniqueId + '.pdf'
        filepath = os.path.join(uploadFilePath, unique_filename)
        file.save(filepath)
        
        # read the file content
        with open(filepath, "rb") as f:
            file_content = f.read()
            f.close()
 
        rowhashText = ai.getDocumentInfos(file_content, openai)
        hashText = hashlib.sha256(rowhashText).hexdigest()
        if eth.checkIfExist(hashText):
            data_response["success"] = False
            data_response["message"] = "The document already exits"
            return data_response
        
        pathOfTheCertifiedDocument = os.path.join(uploadFilePath, uniqueId+"-certified.pdf")
        easyUrlToVerifyTheDocument = f"http://localhost:5500/verify/{hashText}"
        qr.gen_certified_document(hashText, filepath, pathOfTheCertifiedDocument, easyUrlToVerifyTheDocument)

        ipfsIDHash = fs.uploadFile(pathOfTheCertifiedDocument, ipfsBaseUrl)
        eth.saveRecordInBlockChain(ipfsIDHash, hashText)
        
        data_response["success"] = True
        data_response["message"] = "The document is successfully certified."
        data_response["ipfs-url"] = f"http://127.0.0.1:8080/ipfs/{ipfsIDHash}"
        return data_response 
    else:
        data_response["success"] = False
        data_response["message"] = "The file was not uploaded..."
        return data_response

        