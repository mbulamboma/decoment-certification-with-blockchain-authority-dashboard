def checkIfExist(hashText, contract, user_address):
    #get data tasks from blockchain
    return contract.functions.documentExists(hashText).call({'from': user_address})  

def getRecordFromBlockChain(hashText):
    result  =  contract.functions.getDocumentInfo(hashText).call({'from': user_address})  
    datas =  {
            'contentHash': result[0],
            'fileHash': result[1],
            'timestamp': result[2]
        }
    
def saveRecordInBlockChain(ipfsIDHash, hashText, contract, user_address):
    result  =  contract.functions.documentExists(hashText).call({'from': user_address})  
    datas =  {
            'contentHash': result[0],
            'fileHash': result[1],
            'timestamp': result[2]
        }
    return True