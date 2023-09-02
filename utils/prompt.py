prompt_context = 
'''
Return only a JSON format with the following attributes from the transcript document below: "titre_document," "nom_etudiant," "annee_etude," "option," and "annee_academique." Please note that no additional text should be included except for the JSON. 
NOTE: DO NOT PROVIDE ANY OTHER TEXT EXCEPT THE JSON
'''

def getDocumentInfos(content, openai): 
    BIG_PROMPT = prompt_context + content
    response = openai.ChatCompletion.create( model=FINE_TUNED_MODEL,  messages=[{"role": "user", "content": BIG_PROMPT}])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(response.choices[0].message.content)
     try:
        #convert the string to JSON 
        datas =  json.loads(response.choices[0].message.content) 
        rowhashText = datas["titre_document"] + datas["nom_etudiant"] + datas["annee_etude"] + datas["option"] + datas["annee_academique"]
        return rowhashText.lower().replace(" ", "")
    except:
        print("Error: "+str(response.choices[0].message.content))
        return ""