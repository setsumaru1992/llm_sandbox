import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Tell me a joke."}
    ]
)

# print(response)
# ChatCompletion(
#   id='chatcmpl-8qbAD0IzqySbVTHdWaOARKX0h9GYp',
#   choices=[Choice(
#       finish_reason='stop',
#       index=0,
#       logprobs=None,
#       message=ChatCompletionMessage(
#           content="Sure, here's one for you:\n\nWhy don't scientists trust atoms?\n\nBecause they make up everything!",
#           role='assistant',
#           function_call=None, tool_calls=None
#       )
#   )],
#   created=1707546605,
#   model='gpt-3.5-turbo-0613',
#   object='chat.completion',
#   system_fingerprint=None,
#   usage=CompletionUsage(completion_tokens=21, prompt_tokens=22, total_tokens=43))

print(response.choices[0].message.content)
