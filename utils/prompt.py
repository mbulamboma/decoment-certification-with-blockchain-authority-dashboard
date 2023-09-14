prompt_context = '''
Return only a JSON format with the following attributes from the transcript document below: "document_title," "student_name," "academic_year," "option," and "year_of_study." Please note that no additional text should be included except for the JSON. 
NOTE: DO NOT PROVIDE ANY OTHER TEXT EXCEPT THE VALID JSON, AND THE EXTRACTED INFO HAVE TO BE IN UPPER CASE
'''

def getDocumentInfos(content, openai): 
    BIG_PROMPT = prompt_context + content
    response = openai.ChatCompletion.create( model="gpt-3.5-turbo-16k",  messages=[{"role": "user", "content": BIG_PROMPT}])
    return response.choices[0].message.content.lower().replace(" ", "").replace("\n", "")
    