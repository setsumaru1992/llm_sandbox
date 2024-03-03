import os
import json
import pandas as pd
from scipy import spatial
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

domain = "openai.com"
processed_dir = os.path.dirname(__file__) + "/crawl_website/processed"
embedding_csv_path = processed_dir + "/embeddings.csv"

df = pd.read_csv(embedding_csv_path, index_col=0)


# 参照元: https://github.com/openai/openai-cookbook/blob/main/examples/utils/embeddings_utils.py#L138
# embeddings_utilsがOpenAI@v1から消えたらしいため: https://namileriblog.com/python/chatgpt-api-v1x-update/
def distances_from_embeddings(
        query_embedding: List[float],
        embeddings: List[List[float]],
        distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


def create_context(question, df, max_len=1800):
    q_embeddings = client.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding

    df["distances"] = distances_from_embeddings(
        q_embeddings,
        list(map(lambda x: json.loads(x),df["embedding"].values)),
        distance_metric="cosine",
    )

    returns = []
    cur_len = 0
    for i, row in df.sort_values("distances", ascending=True).iterrows():
        cur_len += row["n_tokens"] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="gpt-3.5-turbo",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    debug=False,
    max_tokens=150,
    stop_sequence=None
):
    context = create_context(question, df, max_len=max_len)
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    # try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\n"},
            {"role": "user", "content": f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"}
        ],
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
    )
    return response.choices[0].message.content.strip()
    # except Exception as e:
    #     print(e)
    #     return ""

print(answer_question(df, question="What is ChatGPT?", debug=False))
