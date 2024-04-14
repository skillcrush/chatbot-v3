import time
import random
from openai import OpenAI
import logging
import datetime
import re

log = logging.getLogger("assistant")

logging.basicConfig(filename = "assistant.log", level = logging.INFO)

client = OpenAI()

def process_run(thread_id, assistant_id):
    new_run = client.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id = assistant_id
    )

    phrases = ["Thinking", "Pondering", "Dotting the i's", "Achieving world peace"]

    while True:
        time.sleep(1)
        print(random.choice(phrases) + "...")
        run_check = client.beta.threads.runs.retrieve(
            thread_id = thread_id,
            run_id = new_run.id
        )
        if run_check.status in ["cancelled", "failed", "completed", "expired"]:
            return run_check

def log_run(run_status):
    if run_status in ["cancelled", "failed", "expired"]:
        log.error(str(datetime.datetime.now()) + " Run " + run_status + "\n")

def get_message(run_status):
    if run_status == "completed":
        thread_messages = client.beta.threads.messages.list(
            thread_id = thread.id
        )
        message = thread_messages.data[0].content[0].text.value
        
        if thread_messages.data[0].content[0].text.annotations:
            pattern = r'【\d+†source】'
            message = re.sub(pattern, '', message)


    if run_status in ["cancelled", "failed", "expired"]:
        message = "An error has occurred, please try again."
    
    return message

##### Before push be sure to replace my assistant id with "asst_yournewassistantID"
assistant = client.beta.assistants.retrieve(assistant_id = "asst_FUTO5sCQkGFaK9UAjLCGaWuq")
# print(assistant)
# exit()

# assistant = client.beta.assistants.update(
#     assistant_id = assistant.id,
#     file_ids=[
#         "file-DSfnknuMa6mlrzWihGryKrhl",
#         "file-ukJvh1CTBZiJjPsc0c4CVpwt"
#     ]
# )

# assistant_files = client.beta.assistants.files.list("asst_FUTO5sCQkGFaK9UAjLCGaWuq")
# print(assistant_files)
# exit()


thread = client.beta.threads.create()

user_input = ""

while True:
    if (user_input == ""):
        print("Assistant: Hello there! Just so you know, you can type exit to end our chat. What's your name? ")
        name = input("You: ")
        print("Assistant: Hey, " + name + "! How can I help you?")
        user_input = input("You: ")
    else:
        user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = user_input
    )

    run = process_run(thread.id, assistant.id)

    log_run(run.status)

    message = get_message(run.status)

    print("\nAssistant: " + message + "\n")