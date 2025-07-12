import os
import chainlit as cl
import requests
from dotenv import load_dotenv

load_dotenv()

AGENTFORCE_API_BASE = os.getenv("AGENTFORCE_API_BASE")
ACCESS_TOKEN = os.getenv("SALESFORCE_ACCESS_TOKEN")

def send_to_agentforce(user_message):
    url = f"{AGENTFORCE_API_BASE}/services/apexrest/agentforce/message"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "user_input": user_message
    }

    #try:
        #response = requests.post(url, json=payload, headers=headers, timeout=10)
        #response.raise_for_status()
        #return response.json().get("reply", "No reply from Agentforce.")
    #except Exception as e:
        #return f"Error communicating with Salesforce Agentforce: {e}"

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    await cl.Message(author="User", content=user_input).send()

    bot_reply = send_to_agentforce(user_input)

    await cl.Message(author="Agentforce", content=bot_reply).send()
