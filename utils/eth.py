def checkIfExist(hashText, contract):
    #get data tasks from blockchain
    tasks  = contract.functions.getTasks().call({'from': user_address}) 

    return False

    
def saveRecordInBlockChain(ipfsIDHash, hashText):
    return True