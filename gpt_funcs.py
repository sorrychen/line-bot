import time
import os 
from dotenv import load_dotenv

import re

with open("menu.txt", "r", encoding="utf-8-sig") as menu:
    menu = menu.read().strip()
clean_menu = re.sub(r"^[^\w\n]+", "", menu)




GPT_MODEL = "gpt-4o"
ASSISTANT_NAME = "Cafe Assistant"
ASSISTANT_INSTRUCTIONS = "You are a helpful cafe assistant. 我們的類別有: 咖啡飲品 其他飲品 餐點 甜點 特調 沒有在菜單上的話說沒有, 菜單內容請讀取 menu.txt"
ASSISTANT_INSTRUCTION_WHEN_RUN = "You are a helpful cafe assistant. 我們的類別有: 咖啡飲品 其他飲品 餐點 甜點 特調" + clean_menu

load_dotenv()
GPT_FILE_VECTOR_STORE_ID = os.getenv("GPT_FILE_VECTOR_STORE_ID")

# Step 1: Create an assistant
def create_assistant(client):
    assistant = client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=ASSISTANT_INSTRUCTIONS,
        tools=[{"type": "file_search"}],
        model=GPT_MODEL,
    )
    return assistant.id

# Update assistant
def update_assistant(client, assistant_id):
    assistant = client.beta.assistants.update(
      assistant_id=assistant_id,
      tool_resources={"file_search": {"vector_store_ids": [GPT_FILE_VECTOR_STORE_ID]}},
    )

# Step 2: Create a Thread
def create_thread(client):
    my_thread = client.beta.threads.create()
    print('thread created, thread_id:', my_thread.id)
    return my_thread.id


# Step 3: Add a Message to a Thread
def add_user_message_to_thread(client, thread_id, msg):
    user_message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=msg,
    )
    return user_message


# Step 4: Run
def wait_for_assistant_run(client, thread_id, assistant_id):
    assistant_r = None
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=ASSISTANT_INSTRUCTION_WHEN_RUN
    )
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        print(f'Run status: {run.status}')
        time.sleep(1)
        if run.status == "completed":
            all_messages = client.beta.threads.messages.list(
                thread_id=thread_id
            )
            assistant_r = all_messages.data[0].content[0].text.value
            print(f'Assistant: {assistant_r}')
            break
        elif run.status == 'queued' or run.status == 'in_progress':
            pass
        else:
            print(f'Run status: {run.status}')
            print('create_and_poll again')
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions=ASSISTANT_INSTRUCTION_WHEN_RUN
            )


    return assistant_r
