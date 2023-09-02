import requests

def uploadFile(filepath, ipfsBaseUrl):
    base_url = ipfsBaseUrl
     
    # Charger le fichier que vous souhaitez ajouter
    with open(filepath, "rb") as f:
        file_content = f.read()
        f.close()

    # Envoyer une requête POST pour ajouter le fichier à IPFS
    response = requests.post(
        f"{base_url}/add", files={"file": file_content}
    )

    if response.status_code == 200:
        data = response.json()
        return data["Hash"] 
    else:
        print("Erreur lors de l'ajout :", response.status_code)
        return ""