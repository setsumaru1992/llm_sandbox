import os
import time
import json
from pprint import pprint
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def openai_client() -> OpenAI:
    return client


def fetch_existing_or_create_assistant_id(existing_assistant_id, **params_for_create_assistant):
    return __fetch_existing_or_created_something_id(existing_assistant_id, "assistant_id", client.beta.assistants.create, params_for_create_assistant)


def fetch_existing_or_created_file_id(existing_file_id, **params_for_create_file):
    return __fetch_existing_or_created_something_id(existing_file_id, "file_id", client.files.create, params_for_create_file)


def fetch_existing_or_created_thread_id(existing_thread_id, **params_for_create_thread):
    return __fetch_existing_or_created_something_id(existing_thread_id, "thread_id", client.beta.threads.create, params_for_create_thread)


def __fetch_existing_or_created_something_id(existing_something_id, id_name, create_func, params_for_create):
    if existing_something_id != None:
        return existing_something_id
    created = create_func(**params_for_create)
    print(f"created {id_name}: {created.id}")
    return created.id


def try_variable_length_keyword_args(**keyword_args):
    fuga(**keyword_args)
    # try_variable_length_keyword_args(a=3, b=5) -> エラー無くa,bが印字された
    # try_variable_length_keyword_args(a=3) -> TypeError: fuga() missing 1 required positional argument: 'b'
    # try_variable_length_keyword_args(a=3, b=5, c=4) -> TypeError: fuga() got an unexpected keyword argument 'c'

def fuga(a, b):
    print(a)
    print(b)


def ask_to_assistant(ask_message_content, assistant_id, existing_thread_id = None, **run_params):
    message = {
        "role": "user",
        "content": ask_message_content,
    }
    if existing_thread_id is not None:
        thread_id = existing_thread_id
        client.beta.threads.messages.create(
            thread_id=thread_id,
            **message,
        )
    else:
        thread_id = fetch_existing_or_created_thread_id(None, messages=[message])

    invoke_run(assistant_id, thread_id, run_params)
    assistant_response_messages = client.beta.threads.messages.list(thread_id=thread_id).data
    return assistant_response_messages


def print_assistant_messages(messages):
    # messagesには新しい順、つまり投稿日降順でメッセージが入っている。
    for idx, message in enumerate(messages):
        print(len(messages) - idx, build_print_content_from_assistant_message(message))


def build_print_content_from_assistant_message(message):
    return message.role + ": " + message.content[0].text.value


def invoke_run(assistant_id, thread_id, run_params):
    started_run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    ask_run_status_count = 0
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=started_run.id)

        ask_run_status_count += 1
        if ask_run_status_count % 10 == 0:
            print(f"wait response in {run.status}...")

        if run.status in ["queued", "in_progress", "cancelling"]:
            time.sleep(0.5)
        elif run.status == "completed":
            break
        elif run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in tool_calls:
                function = run_params["available_functions"][tool_call.function.name]
                arguments = json.loads(tool_call.function.arguments)

                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=started_run.id,
                    tool_outputs=[{
                        "tool_call_id": tool_call.id,
                        "output": function(**arguments)
                    }]
                )
                print(f"func call: {tool_call.function.name}(#**{arguments})")
            pass
        elif run.status in ["cancelled", "failed", "expired"]:
            break
        else:
            pass