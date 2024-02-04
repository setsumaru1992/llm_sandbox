from openai import OpenAI

client = OpenAI(api_key='YOUR_API_KEY')

# OpenAI APIキーを設定

response = client.chat.completions.create(model="gpt-3.5-turbo",  # 使用するモデルを指定
messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Tell me a joke."}
  ])

print(response.choices[0].message.content)

