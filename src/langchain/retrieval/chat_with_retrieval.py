import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import chainlit as cl

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(
    persist_directory=os.path.dirname(__file__) + "/.data",
    embedding_function=embeddings
)

template = """
文章を元に質問に答えてください。

文章:
{document}

質問: {query}
"""
prompt = PromptTemplate(
    template=template,
    input_variables=["document", "query"]
)

chat = ChatOpenAI(model="gpt-3.5-turbo")

# chat開始は`chainlit run chat_with_retrieval.py`
@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="準備ができました！メッセージを入力してください！").send()

@cl.on_message
async def on_message(input_message):
    print("入力されたメッセージ: " + input_message.content)

    documents = database.similarity_search(input_message.content)
    documents_string = ""
    for document in documents:
        documents_string += f"""
    ------
    {document.page_content}    
    """

    result = chat.invoke([
        HumanMessage(content=prompt.format(
            document=documents_string,
            query=input_message.content
        ))
    ])
    await cl.Message(content=result.content).send()