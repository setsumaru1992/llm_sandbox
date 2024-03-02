# 公式ドキュメントだとエッセンスのみで詳細のコードが無かったから、以下を写経
# https://zenn.dev/umi_mori/articles/openai-chatgpt-assistants-api
import os
from functions import (
    openai_client,
    fetch_existing_or_create_assistant_id,
    fetch_existing_or_created_file_id,
    ask_to_assistant,
    print_assistant_messages,
)

client = openai_client()

knowledge_file_id = fetch_existing_or_created_file_id(
    os.getenv("FILE_ID_OF_USE_RERIEVAL"),
    file=open(os.path.dirname(__file__) + "/飛行車.pdf", "rb"),
    purpose="assistants"
)

assistant_id = fetch_existing_or_create_assistant_id(
    os.getenv("ASSISTANT_ID_OF_USE_RERIEVAL"),
    name="Flying car expert",
    description="飛行車についてドキュメントに基づいた知識に基づいて回答するエキスパート",
    model="gpt-4-1106-preview",
    instructions="あなたは新製品「飛行車」について詳しいアシスタントです。飛行車の教材を参考にして回答してください",
    tools=[{"type": "retrieval"}],
    file_ids=[knowledge_file_id],
)

messages = ask_to_assistant("飛行車の最高速度は？", assistant_id)
print_assistant_messages(messages)

# assistant: 飛行車の最高速度は、都市部では時速150キロメートル、都市部以外の地域では時速250キロメートルと制限されています【7†source】。
# user: 飛行車の最高速度は？

# 参考にしたサイトによると、LangChainでassistant使えるらしい
# from langchain.agents.openai_assistant import OpenAIAssistantRunnable
# my_assistant = OpenAIAssistantRunnable.create_assistant(
#
# ただ、langchainで使いやすい形で呼んでくれるというより、langchain経由で単にassistant呼ぶだけっぽい
# https://python.langchain.com/docs/modules/agents/agent_types/openai_assistants