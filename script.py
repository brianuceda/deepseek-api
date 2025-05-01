from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-dd557453093d48aea7429b5f094197ad",
    base_url="https://api.deepseek.com"
)

def deepseek(model="deepseek-chat", max_tokens=1000, temperature=0.7, message=None):
    try:
        if message is None or message == "":
            raise Exception("Message is required")
        if model is None or model == "" or (model != "deepseek-chat" and model != "deepseek-reasoner"):
            raise Exception("Invalid model")
        
        response = client.chat.completions.create(
            # deepseek-chat: DeepSeek-V3
            # deepseek-reasoner: DeepSeek-R1
            model=model,
            messages=[
                {"role": "user", "content": message}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        return response.choices[0].message.content
    except Exception as e:
        error = json.loads(str(e).split(" - ")[1].replace("'", "\"").replace("None", "null"))
        error['error']['code'] = str(e).split(" - ")[0].split(": ")[1]
        error['error']['message'] = error['error']['message']
        error['error'].pop('param')
        error['error'].pop('type')
        return json.dumps(error['error'], indent=2)

def main():
    call = deepseek(message="Cuál es la fecha de hoy?")
    print(call)
    
if __name__ == "__main__":
    main()
