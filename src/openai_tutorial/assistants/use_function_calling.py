import os
import json
from functions import (
    openai_client,
    fetch_existing_or_create_assistant_id,
    ask_to_assistant,
    print_assistant_messages,
)

client = openai_client()

assistant_id = fetch_existing_or_create_assistant_id(
    os.getenv("ASSISTANT_ID_OF_USE_FUNCTION_CALLING"),
    name="Weather expert",
    instructions="You are a weather bot. Use the provided functions to answer questions.",
    model="gpt-4-1106-preview",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "getCurrentWeather",
                "description": "Get the weather in Location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                        "unit": {"type": "string", "enum": ["c", "f"]},
                    },
                    "required": ["location"],
                },
            },
        },
    ]
)


def get_current_weather(location, unit="f"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


messages = ask_to_assistant(
    "Tell me today's weather in San Francisco.", # FunctionCallingがされる問い
    # "How is water written in Japanese?", # FunctionCallingがされない問い
    assistant_id,
    available_functions = {
        "getCurrentWeather": get_current_weather
    }
)
print_assistant_messages(messages)

# assistantsのFunctionCallingは自身が実行できる関数を実行する機能
#   予約された関数について、回答に実行が必要なら実行時の引数とともに渡してくれて、こちらの実行を待ってくれる。
#   好例としてGUIのAssistantのPlaygroundでFunctionCallingが必要なやつ実行すると関数のアウトプットの入力が求められる
# GPTsで対応しているActionが外部URL(API)を指定しているのは、
#   GPTはGUIでプログラムを持てないから、公開された関数としての外部URLを必要とするのね
