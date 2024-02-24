from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？",
    input_variables=["product"]
)

chain = LLMChain(llm=chat, prompt=prompt, verbose=True)
print(chain.predict(product="iPhone"))