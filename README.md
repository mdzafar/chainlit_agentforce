# Chainlit Agentforce Chat UI

This is a simple Chainlit app [Chainlit](https://www.chainlit.io/) that connects a chat interface to Salesforce Agentforce using REST API.

## Features

- Chat UI with Chainlit
- Connects to Salesforce Agentforce
- OAuth 2.0 client credentials flow
- Real-time message handling

## Setup

### 1. Clone and enter project

```bash
git clone https://github.com/mdzafar/chainlit_agentforce.git
cd chainlit_agentforce
```

### 2. Create & activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Copy the example and edit:

```bash
cp .env.example .env
```

Fill in the Salesforce API credentials in `.env`.

```
BASE_URL=https://your.salesforce.instance
AGENT_API_BASE_URL=https://your.salesforce.instance/services/...
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
AGENT_ID=your_agentforce_agent_id
```

### 5. Run the app

```bash
chainlit run main.py
```

Open `http://localhost:8000` or preview in Codespaces.

## Files

- `main.py` - Chat logic and API integration
- `.env.example` - Environment config sample
- `.chainlit/config.toml` - Chainlit project settings
