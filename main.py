import os
import uuid
import datetime
import time
import json
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
AGENT_API_BASE_URL = os.getenv("AGENT_API_BASE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AGENT_ID = os.getenv("AGENT_ID")
#USERNAME = os.getenv("USERNAME")
#PASSWORD = os.getenv("PASSWORD")

# Generate a random UUID
def generate_random_uuid():
    return str(uuid.uuid4())

def get_current_timestamp():
    return int(time.time())

def authenticate():
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
        #'username': USERNAME,
        #'password': PASSWORD
    }
    response = requests.post(f"{BASE_URL}/services/oauth2/token", data=payload)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        return None
    
def start_session():
    global global_session_id, global_access_token
    access_token = authenticate();
    if not access_token:
        return "Authentication failed!"

    global_access_token = access_token;

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    session_payload = {
        "externalSessionKey": generate_random_uuid(),
        "instanceConfig": {
            "endpoint": BASE_URL
        },
        "variables": [],
        "streamingCapabilities": {
            "chunkTypes": ["Text"]
        },
        "bypassUser": 'false'
    }
    response = requests.post(f"{AGENT_API_BASE_URL}/agents/{AGENT_ID}/sessions", headers=headers, json=session_payload)
    if response.status_code == 200:
        session_id = response.json().get("sessionId")
        global_session_id = session_id;
        return "Session started successfully!"
    else:
        return "Failed to start session!"
    
def send_synchronous_message(message):

    headers = {
        "Authorization": f"Bearer {global_access_token}",
        "Content-Type": "application/json"
    }

    message_payload = {
        "message": {
            "sequenceId": get_current_timestamp(),
            "type": "Text",
            "text": message
          },
        "variables": []
    }

    response = requests.post(f"{AGENT_API_BASE_URL}/sessions/{global_session_id}/messages", headers=headers, json=message_payload)

    if response.status_code == 200:
      message_data = response.json();
      return message_data["messages"][0]["message"]
    else:
      return "Failed to send synchronous message!"

# def send_to_agentforce(user_message):
#     url = f"{AGENTFORCE_API_BASE}/services/apexrest/agentforce/message"
#     headers = {
#         "Authorization": f"Bearer {ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "user_input": user_message
#     }

#     #try:
#         #response = requests.post(url, json=payload, headers=headers, timeout=10)
#         #response.raise_for_status()
#         #return response.json().get("reply", "No reply from Agentforce.")
#     #except Exception as e:
#         #return f"Error communicating with Salesforce Agentforce: {e}"

@cl.on_chat_start
def on_chat_start():
    start_session()
    print(start_session())


@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content
    await cl.Message(author="User", content=user_input).send()

    bot_reply = send_synchronous_message(user_input)

    await cl.Message(author="Agentforce", content=bot_reply).send()
