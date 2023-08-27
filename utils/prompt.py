prompt_context = """From the below document retrieve in json format Nom de l'Etudiant, Titre du document, 

"""

def getDocumentInfos(content, openai):
    BIG_PROMPT = prompt_context + content
    response = openai.ChatCompletion.create( model=FINE_TUNED_MODEL,  messages=[{"role": "user", "content": BIG_PROMPT}])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(response.choices[0].message.content)
     try:
        #convert the string to JSON 
        return json.loads(response.choices[0].message.content)        
    except:
        print("Error: "+str(response.choices[0].message.content))
        return {}