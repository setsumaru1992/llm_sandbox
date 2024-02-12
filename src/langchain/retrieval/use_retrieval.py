import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(
    persist_directory=os.path.dirname(__file__) + "/.data",
    embedding_function=embeddings
)

query = "飛行車の最高速度は？"
documents = database.similarity_search(query)
# print(f"ドキュメントの数: {len(documents)}")

documents_string = ""
for document in documents:
    # print(f"ドキュメントの内容: {document.page_content}")
    documents_string += f"""
------
{document.page_content}    
"""

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
result = chat.invoke([
    HumanMessage(content=prompt.format(
        document=documents_string,
        query=query
    ))
])
print(result.content)

# これもいいけど、RetrievalQAを使うとスマートに書ける(参考: use_qa_retriever.py)