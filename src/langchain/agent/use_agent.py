import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools

load_dotenv()

# 2024.2.12時点、3章のRetrievalまでしか終わってないけど、requestsを使いたいので一旦先取り。
# requestsでapi以外のhtml触れるか試せたら戻る

agent = initialize_agent(
    tools=load_tools(["requests_all"]),
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0),
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# instruction = """
# 以下のURLにアクセスして、東京の天気を調べて日本語で調べてください。
# https://www.jma.go.jp/bosai/forecast/data/overview_forecast/130000.json
# """

# instruction = """
# 以下のURLにアクセスして、railsの最新のバージョンを調べて日本語で調べてください。
# https://rubygems.org/gems/rails/versions/7.1.3
# """
# →長すぎてアクセスできない
# openai.BadRequestError: Error code: 400 - {'error': {'message': "This model's maximum context length is 4097 tokens. However, your messages resulted in 10939 tokens. Please reduce the length of the messages.", 'type': 'invalid_request_error', 'param': 'messages', 'code': 'context_length_exceeded'}}

instruction = """
以下のURLにアクセスして、どのようなサイトか教えて下さい。
https://example.com/
"""
# →短ければ実行可能
# 実行結果: {
#   'input': '\n以下のURLにアクセスして、どのようなサイトか教えて下さい。\nhttps://example.com/\n',
#   'output': 'The website at the URL "https://example.com/" is a generic example domain.'
# }

result = agent.invoke(instruction)

print(f"実行結果: {result}")