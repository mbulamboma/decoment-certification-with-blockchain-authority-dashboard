import json
from datetime import datetime

def getAbiAndContractAddr(abi_file_path):
    with open(abi_file_path) as f:
        datas = json.load(f)
        contract_abi = datas["abi"]
        contract_address = datas["networks"]["5777"]["address"]
    return contract_abi, contract_address
 

def getCurrentTime():
    current_datetime = datetime.now()
    # Format the date and time as "dd-mm-yy hh:mm"
    formatted_datetime = current_datetime.strftime("%d-%m-%y %H:%M")
    return str(formatted_datetime)