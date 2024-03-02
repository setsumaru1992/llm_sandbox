import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

assistant_id = os.getenv("ASSISTANT_ID_OF_USE_ASSISTANT")
if assistant_id == None:
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4-turbo-preview",
    )
    print(assistant.id)
    assistant_id = assistant.id

thread_id = None
if thread_id == None:
    thread = client.beta.threads.create()
    print("thread_id: " + thread.id)
    thread_id = thread.id

message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
# print(message)

run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="Please address the user as Jane Doe. The user has a premium account",
)

while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread_id,run_id=run.id)
    if run.status in ["queued", "in_progress", "cancelling"]:
        time.sleep(0.1)
    elif run.status == "completed":
        break
    elif run.status == "requires_action":
        # Handle tool calls (see below)
        pass
    elif run.status in ["cancelled", "failed", "expired"]:
        break

message_obj = client.beta.threads.messages.list(thread_id=thread_id)
# print(type(message_obj)) # <class 'openai.pagination.SyncCursorPage[ThreadMessage]'>
for message in message_obj.data:
    print(message.role + ": " + message.content[0].text.value)

# print(message_obj)
# SyncCursorPage[ThreadMessage](data=[
#   ThreadMessage(
#       id='msg_A5OOo1rEXUdCVC6kecmfjQdU', assistant_id='...',
#       content=[MessageContentText(text=Text(annotations=[], value="Is there anything else you'd like to solve or any other question I can assist you with?"), type='text')],
#       created_at=1708786748, file_ids=[], metadata={}, object='thread.message', role='assistant', run_id='run_QQpCvIdnryeyvFAb4IX4gJ1P', thread_id='...'),
#   ThreadMessage(id=...,
#   object='list', first_id='msg_A5OOo1rEXUdCVC6kecmfjQdU', last_id='msg_cDDCWAkOIah9ThmuLPmZFuzx', has_more=False)