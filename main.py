import os
import uuid
import time
import requests
import chainlit as cl
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
AGENT_API_BASE_URL = os.getenv("AGENT_API_BASE_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AGENT_ID = os.getenv("AGENT_ID")

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
    }
    try:
        response = requests.post(f"{BASE_URL}/services/oauth2/token", data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except Exception as e:
        print(f"Auth error: {e}")
        return None
    
def start_session(access_token):
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

    try:
        response = requests.post(
            f"{AGENT_API_BASE_URL}/agents/{AGENT_ID}/sessions",
            headers=headers,
            json=session_payload
        )
        response.raise_for_status()
        return response.json().get("sessionId")
    except Exception as e:
        print(f"Session error: {e}")
        return None
    
def send_synchronous_message(access_token, session_id, message):
    headers = {
        "Authorization": f"Bearer {access_token}",
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

    try:
        response = requests.post(
            f"{AGENT_API_BASE_URL}/sessions/{session_id}/messages",
            headers=headers,
            json=message_payload
        )
        response.raise_for_status()
        return response.json()["messages"][0]["message"]
    except Exception as e:
        print(f"Message send error: {e}")
        return "Sorry, I couldn’t reach the Agentforce backend."

# Chainlit event: chat start
@cl.on_chat_start
async def on_chat_start():
    access_token = authenticate()
    session_id = start_session(access_token)

    if not access_token or not session_id:
        await cl.Message(content="Could not start session with Agentforce. Please check config.").send()
        return

    # Save to Chainlit user session state
    cl.user_session.set("access_token", access_token)
    cl.user_session.set("session_id", session_id)

    await cl.Message(content="Connected to Agentforce. How can I help you today?").send()

# Chainlit event: on message
@cl.on_message
async def handle_message(message: cl.Message):
    access_token = cl.user_session.get("access_token")
    session_id = cl.user_session.get("session_id")

    if not access_token or not session_id:
        await cl.Message(content="Session is not initialized. Please refresh the chat.").send()
        return

    user_input = message.content
    reply = send_synchronous_message(access_token, session_id, user_input)

    await cl.Message(author="Agentforce", content=reply).send()
