prompt_context = '''
Return only a JSON format with the following attributes from the transcript document below: "titre_document," "nom_etudiant," "annee_etude," "option," and "annee_academique." Please note that no additional text should be included except for the JSON. 
NOTE: DO NOT PROVIDE ANY OTHER TEXT EXCEPT THE VALID JSON
'''

def getDocumentInfos(content, openai): 
    BIG_PROMPT = prompt_context + content
    response = openai.ChatCompletion.create( model="gpt-3.5-turbo-16k",  messages=[{"role": "user", "content": BIG_PROMPT}])
    return response.choices[0].message.content.lower().replace(" ", "")
    