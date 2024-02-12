import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import WikipediaRetriever
from langchain.chains import RetrievalQA

load_dotenv()

retriever = WikipediaRetriever(
    lang="ja",
    doc_content_chars_max=500,
    top_k_result=2,
)

# documents = retriever.get_relevant_documents("大規模言語モデル")
# print(f"検索結果: {len(documents)}件")
# for document in documents:
#     print("---- 取得したメタデータ ----")
#     print(document.metadata)
#     print("---- 取得したテキスト ----")
#     print(document.page_content[:100])

ask = RetrievalQA.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=retriever,
    return_source_documents=True,
)

response_from_ask = ask("バーボンウイスキーとは？")

print("---- 返答 ----")
print(response_from_ask["result"])
print("")

source_documents = response_from_ask["source_documents"]
print(f"検索結果: {len(source_documents)}件")
for document in source_documents:
    print("---- 取得したメタデータ ----")
    print(document.metadata)
    print("---- 取得したテキスト ----")
    print(document.page_content[:100])