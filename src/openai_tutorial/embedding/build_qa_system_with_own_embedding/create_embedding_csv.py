import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
import matplotlib.pyplot as plt
import tiktoken

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

domain = "openai.com"
crawl_result_dir = os.path.dirname(__file__) + "/crawl_website/text"
crawl_result_dir_with_domain = crawl_result_dir + "/" + domain
processed_dir = os.path.dirname(__file__) + "/crawl_website/processed"
scraped_csv_path = processed_dir + "/scraped.csv"
sample_scraped_csv_path = processed_dir + "/sample_scraped.csv"
embedding_csv_path = processed_dir + "/embeddings.csv"

tokenizer = tiktoken.get_encoding("cl100k_base")


def remove_newlines(serie):
    serie = serie.str.replace("\n", " ")
    serie = serie.str.replace("\\n", " ")
    serie = serie.str.replace("  ", " ")
    serie = serie.str.replace("  ", " ")
    return serie


def create_scraped_csv():
    texts = []
    for file in os.listdir(crawl_result_dir_with_domain):
        with open(crawl_result_dir_with_domain + "/" + file, "r", encoding="UTF-8") as f:
            text = f.read()
            texts.append((file[11:-4].replace("-", " ").replace("_", " ").replace("#update", ""), text))

    df = pd.DataFrame(texts, columns=["fname", "text"])
    df["text"] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv(scraped_csv_path)
    print(df.head())


# create_scraped_csv()

max_tokens = 500


def split_text_into_tokens(text, max_tokens = max_tokens):
    sentences = text.split(". ")
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue

        chunk.append(sentence)
        tokens_so_far += token + 1
    return chunks


def convert_long_texts_into_readable_chunks(long_texts_df):
    long_texts_df.columns = ["title", "text"]
    long_texts_df["n_tokens"] = long_texts_df.text.apply(lambda x: len(tokenizer.encode(x)))

    # df.n_tokens.hist()
    # plt.show()

    shortened = []

    for row in long_texts_df.iterrows():
        text = row[1]["text"]
        if text is None:
            continue
        if row[1]["n_tokens"] > max_tokens:
            shortened += split_text_into_tokens(text)
        else:
            shortened.append(text)

    shortened_df = pd.DataFrame(shortened, columns = ["text"])
    shortened_df["n_tokens"] = shortened_df.text.apply(lambda  x: len(tokenizer.encode(x)))
    # shortened_df.n_tokens.hist()
    # plt.show()
    return shortened_df


# 料金
# $0.02 / 1Mトークン
# - sample_scraped_csv_path (元々のopenai.comの1274ページの先頭100ページを抜粋)
#   - 129,705トークン
def create_embedding_csv(scraped_csv_path):
    scraped_df = pd.read_csv(scraped_csv_path, index_col=0)
    shortened_df = convert_long_texts_into_readable_chunks(scraped_df)

    shortened_df["embedding"] = shortened_df.text.apply(
        lambda x: client.embeddings.create(input=x, model="text-embedding-3-small").data[0].embedding
    )
    shortened_df.to_csv(embedding_csv_path)
    print(shortened_df.head())


create_embedding_csv(sample_scraped_csv_path)
