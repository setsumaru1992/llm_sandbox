from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

# OpenAI APIキーを設定

response = client.chat.completions.create(model="gpt-3.5-turbo",  # 使用するモデルを指定
messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Tell me a joke."}
  ])

print(response.choices[0].message.content)

