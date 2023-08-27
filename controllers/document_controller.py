
import hashlib
from utils import qrcode as qr

def certify(request, uploadFilePath):
    file = request.files['myFile']
    # 1. extract useful information about the document form OpenAI
    # 2. treat the extracted String
    rowhashText = "Text Gotten from OpenAi"
    hashText = hashlib.sha256(rowhashText).hexdigest()

    if file:
        uniqueId = str(uuid.uuid4())
        unique_filename = uniqueId + '.pdf'
        filepath = os.path.join(uploadFilePath, unique_filename)
        file.save(filepath)
        # 2.4 Extract from the document useful information
        # 2.5 Check if in the blockchain has the similar record
        pathOfTheCertifiedDocument = os.path.join(uploadFilePath, uniqueId+"-certified.pdf")
        easyUrlToVerifyTheDocument = "https://localhost/Generate-the-Url-for-verification"
        qr.gen_certified_document(hashText, filepath, pathOfTheCertifiedDocument, easyUrlToVerifyTheDocument)

        # 3. now Send the Certified Document to a Decentralized Network
        # 4. Save All the information in the blockchain

        