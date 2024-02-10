from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo")
result = chat.invoke([HumanMessage(content="こんにちは！")])

print(result.content)