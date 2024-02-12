import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(
    persist_directory=os.path.dirname(__file__) + "/.data",
    embedding_function=embeddings
)
retriever = database.as_retriever()

qa = RetrievalQA.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=retriever,
    return_source_documents=True,
)
result = qa("飛行車の最高速度を教えて")
print(result["result"])
print(result["source_documents"])