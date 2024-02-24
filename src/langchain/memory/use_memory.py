from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain
import chainlit as cl

load_dotenv()

chat = ChatOpenAI(model="gpt-3.5-turbo")


# chat開始は`chainlit run user_memory.py`

# memory = ConversationBufferMemory(return_messages=True)
#
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。").send()
#
# @cl.on_message
# async def on_message(message: str):
#     memory_message_result = memory.load_memory_variables({})
#     messages = memory_message_result["history"]
#
#     messages.append(HumanMessage(content=message.content))
#
#     result = chat(messages)
#
#     memory.save_context(
#         {"input": message.content},
#         {"output": result.content},
#     )
#     await cl.Message(content=result.content).send()


# chain = ConversationChain(
#     memory=ConversationBufferMemory(return_messages=True),
#     llm=chat
# )
#
# @cl.on_chat_start
# async def on_chat_start():
#     await cl.Message(content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。").send()
#
# @cl.on_message
# async def on_message(message):
#     result = chain(message.content)
#     await cl.Message(content=result["response"]).send()


# memory = ConversationBufferWindowMemory(return_messages=True, k=3)
memory = ConversationSummaryMemory(return_messages=True, llm=chat)
chain = ConversationChain(memory=memory, llm=chat)

@cl.on_chat_start
async def on_chat_start():
    await cl.Message(content="私は会話の文脈を考慮した返答ができるチャットボットです。メッセージを入力してください。").send()

@cl.on_message
async def on_message(message: str):
    messages = memory.load_memory_variables({})["history"]

    print(f"保存されているメッセージの数", {len(messages)})

    for saved_message in messages:
        print(saved_message.content)
    result = chain(message.content)
    await cl.Message(content=result["response"]).send()