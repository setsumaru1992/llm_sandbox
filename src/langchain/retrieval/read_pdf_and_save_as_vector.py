import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import SpacyTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

documents = PyMuPDFLoader(os.path.dirname(__file__) + "/sample.pdf").load()

# print(f"ドキュメントの数: {len(documents)}")
# print(f"1つ目のドキュメントの内容: {documents[0].page_content}")
# print(f"1つ目のドキュメントのメタデータ: {documents[0].metadata}")

text_splitter = SpacyTextSplitter(
    chunk_size=300,
    pipeline="ja_core_news_sm"
)
split_documents = text_splitter.split_documents(documents)

# print(f"分割前のドキュメントの数: {len(documents)}")
# print(f"分割後のドキュメントの数: {len(split_documents)}")

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(
    persist_directory=os.path.dirname(__file__) + "/.data",
    embedding_function=embeddings
)
database.add_documents(split_documents)
print("データベースの作成が完了しました")
