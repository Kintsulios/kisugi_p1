import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Error")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-20b"
role="user"

from pydantic import BaseModel
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema=Ticket.model_json_schema()

response_format={
    "type":"json_object"
}

system_prompt=f"""
Extract me response strictly based on this schema and give me output in proper json format
 {schema}
"""
message_system={
    "role":"system",
    "content":system_prompt
}

text="Hey my name is surya and i bought an iphone from your store which is not working at all. my address is banglore and my phone number is 9999 and my email is abc@anything.com."

prompt=f"""
Extract the  personal details from this{text}
"""

message={
    "role":role,
    "content":prompt 
}
messages=[message_system,message]
response=client.chat.completions.create(model=model,messages=messages, response_format=response_format,temperature=2)
#print(response)

#print("################################################################")
answer=response.choices[0].message.content
print(answer)


import json 

raw_json=answer 
data_file=json.loads(raw_json)

ticket=Ticket(**data_file)

print(ticket.name)
print(ticket.issue)
print(ticket.email)


#Homework

# take resume in pdf or word
# have hr give you a list of things like skill, experience, projects
# extract these from resume
# match against the hr list
# generate a percentage of matching or not

