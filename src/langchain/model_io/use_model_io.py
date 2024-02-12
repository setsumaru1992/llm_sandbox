import time
import langchain
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.cache import InMemoryCache
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

load_dotenv()
langchain.llm_cache = InMemoryCache()
is_array_output = False


chat = ChatOpenAI(
    model="gpt-3.5-turbo",
    # streaming=True,
    # callbacks=[
    #     StreamingStdOutCallbackHandler()
    # ],
)

# messages = [HumanMessage(content="おいしいステーキの焼き方を教えて")] # StreamingStdOutCallbackHandlerの設定といっしょに使用

# AIメッセージ
# messages = [
#     HumanMessage(content="茶碗蒸しの作り方を教えて"),
#     AIMessage(content="{ChatModelからの返答である茶碗蒸しの作り方}"),
#     HumanMessage(content="英語に翻訳して"),
# ]

# システムメッセージ: 言語への直接の指示
# messages = [
#     SystemMessage(content="あなたは親しい友人です。返答は敬語を使わず、フランクに会話してください"),
#     HumanMessage(content="こんにちは！"),
# ]

prompt = PromptTemplate(
    template="{product}はどこの会社が開発した製品ですか？",
    input_variables=["product"]
)
messages = [
    HumanMessage(content=prompt.format(product="iPhone")),
]


output_parser = None
# output_parser = CommaSeparatedListOutputParser()
# messages = [
#     HumanMessage(content="Appleが開発した代表的な製品を3つ教えて下さい"),
#     HumanMessage(content=output_parser.get_format_instructions()), # 「アウトプットをカンマ区切りで出して」と指示
# ]
# is_array_output = True

llm = None
formatted_prompt = None
# few_shot_prompt = FewShotPromptTemplate(
#     examples=[
#         {
#             "input": "LangChainはChatGPT・Large Language Model(LLM)の実利用をより柔軟に簡易に行うためのツール群です",
#             "output": "LangChainは、ChatGPT・Large Language Model(LLM)の実利用をより柔軟に、簡易に行うためのツール群です。"
#         }
#     ],
#     example_prompt=PromptTemplate(
#         input_variables=["input", "output"],
#         template="入力: {input}\n出力: {output}"
#     ),
#     prefix="以下の句読点の抜けた入力に句読点を追加してください。追加して良い句読点は「、」「。」のみです。他の句読点は追加しないでください。",
#     suffix="入力: {input_string}\n出力:",
#     input_variables=["input_string"],
# )
# formatted_prompt = few_shot_prompt.format(
#     input_string="私はさまざまな機能がモジュールとして提供されているLangChainを使ってアプリケーションを開発しています"
# )
# chat = None
# llm = OpenAI()

if llm != None:
    print(
        formatted_prompt, # テンプレートと言っておきながら、テンプレート内では後述のinvoke結果は含めずお膳立て文言を出力する
        llm.invoke(formatted_prompt)
    )

if chat != None:
    result = chat.invoke(messages)
    print(result.content)
    if is_array_output:
        [print("代表的な製品 => " + output) for output in output_parser.parse(result.content)]
