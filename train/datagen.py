import os
import json
import time
import requests
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv()

API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_CONTENT = '''
You are an AI model that can generate unlimited short independent conversational clips between a chatbot and farmer users. The clips you can generate are really short, of the form "Question, Answer, Question". You always output these conversations in following json format:
[
  {
    "Input": "User: How to control pests in my apple orchard? AI: You can use Integrated Pest Management (IPM), which combines different pest control methods and reduces the use of chemical pesticides in your apple orchard. User: Can you suggest some IPM methods suitable for above?",
    "Output": "User: Can you suggest some Integrated Pest Management (IPM) pest control methods suitable for my apple orchard?"
  },
  {
    "Input": "User: What is the ideal temperature for growing tomatoes? AI: The ideal temperature for growing tomatoes is between 21-27°C. User: And what about the soil pH level?",
    "Output": "User: And what about the ideal soil pH level for growing tomatoes?"
  },
  {
    "Input: "User: Why is my peach tree not producing fruit? AI: Lack of fruit can be due to poor pollination, insufficient chill hours, or nutrient imbalances. User: How to ensure enough chill hours?",
    "Output": "User: How can I ensure my peach tree gets enough chill hours to produce fruit?"
  },
  ...
]
The Output contains the final User question modified by including contextual information required for the chatbot to generate an accurate answer. The Output has all coreferences and ambiguities resolved and can completely capture the intention of the User's final question in Input. You can generate 10 percent of the conversations with User's using bad English in Input questions but the Output should be very clear anyway. You can generate all kinds of complex Inputs with valid questions but Output should focus on making the last user question clear specifying what is required to resolve the context to make the question more clear for the chatbot to get an accurate answer from it.
You will be provided with timestamps in the prompt so as to not generate same examples again. Function like a random generator but with timestapms as seed values.
'''

def generate_chat_completion(user_content, model="gpt-3.5-turbo", temperature=1, top_p=1, max_tokens=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_CONTENT },
            {"role": "user", "content": user_content}
        ],
        "temperature": temperature,
        # "top_p": top_p
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

if not os.path.exists("./train.json"):
    with open("./train.json", 'w') as f:
        json.dump({"data": []}, f)

with open("./train.json", 'r') as f:
  data = json.load(f)

for i in tqdm(range(2)):
    try:
        time_stamp = str(int(time.time()))
        res = generate_chat_completion(f"Timestamp = {time_stamp}, Generate 20 samples focusing on Indian agriculture, in the format of how samples are listed, i.e., list of json objects having Input, Output and nothing extra. The samples should cover a wide range of conversations, include a wide range of vocabulary and different types of questions. No two samples generated should be similar to one another.")
        res = json.loads(res)
        for item in res:
            if "Input" not in item or "Output" not in item:
                raise Exception("Input/Output not in item")
            try:
                item["Input"].split('User: ')[1].split('AI: ')[0]
                item["Input"].split('AI: ')[1].split('User: ')[0]
                item["Input"].split('User: ')[2]
                item["Output"].split('User: ')[1]
            except:
                raise Exception("Q A Q not generated.")
        data["data"].extend(res)
    except:
        print("Error in i/o (or) loading json")

with open("./train.json", 'w') as f:
   json.dump(data, f)
