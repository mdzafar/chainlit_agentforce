# Chainlit Agentforce Chat UI

This is a simple Chainlit app that connects a chat interface to Salesforce Agentforce using REST API.

## Setup

1. Create `.env` file with your Salesforce credentials:
```
AGENTFORCE_API_BASE=https://your-instance.salesforce.com
SALESFORCE_ACCESS_TOKEN=your_oauth_token
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
chainlit run main.py
```

Then open `http://localhost:8000` in your browser.

## Project Structure

```
chainlit_agentforce/
├── main.py
├── .env
├── requirements.txt
├── README.md
└── .chainlit/
    └── config.toml
```
