# Importaciones
import pandas as pd # type: ignore
import time
import sys
sys.path.append("../")

import os
import dotenv # type: ignore
dotenv.load_dotenv()
from openai import OpenAI # type: ignore

def init_openai():
    os.getenv("OPENAI_API_KEY")
    return OpenAI()

def list_asisstants(openai_client):
    return  openai_client.beta.assistants.list(
        order="desc",
        limit="20",
    )

def get_assistant(openai_client, assistant_id):
    return openai_client.beta.assistants.retrieve(
        assistant_id=assistant_id
    )

def create_thread(openai_client):
    return openai_client.beta.threads.create()

def process_data(openai_client, assistant_id, thread_id, message):

    openai_client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    run = openai_client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_status = openai_client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
    )

    while True:
        run_status = openai_client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == "completed":
            print("se completó exitosamente.")
            break
        elif run_status.status == "failed":
            print("falló.")
            break
        else:
            print("Esperando a que se complete...")
            time.sleep(2)

    print(f"Thread ID: {thread_id}")
    print(f"Run ID: {run.id}")
    print(f"Run Status: {run_status.status}")

    response_messages = openai_client.beta.threads.messages.list(thread_id=thread_id)

    assistant_response = None
    for message in response_messages.data:
        if message.role == "assistant":
            assistant_response = "\n".join([block.text.value for block in message.content])
            break

    if assistant_response:
        print(f"Respuesta del asistente:\n{assistant_response}")
    else:
        print("No se encontró una respuesta del asistente.")



