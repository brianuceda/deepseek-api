import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")
model = os.getenv("MODEL")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def chat(temperature=0.7, message=None):
    try:
        if message is None or message == "":
            raise Exception("Message is required")
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            temperature=temperature
        )
        
        return response.choices[0].message.content
    except Exception as e:
        try:
            error = json.loads(str(e).split(" - ")[1].replace("'", "\"").replace("None", "null"))
            error['error']['code'] = str(e).split(" - ")[0].split(": ")[1]
            error['error']['message'] = error['error']['message']
            error['error'].pop('param')
            error['error'].pop('type')
            return json.dumps(error['error'], indent=2)
        except Exception as e:
            return str(e)

def main():
    instructions = [
        'Solo dime el resultado de la solicitud, no hagas preguntas al usuario',
    ]
    instructions = "Estas son las instrucciones: " + ". ".join(instructions) + ". Esta es la solicitud formal: "
    
    message = "Dime que fecha es hoy"
    message = instructions + message
    
    response = chat(message=message)
    
    print(response)
    
if __name__ == "__main__":
    main()
