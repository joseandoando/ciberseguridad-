# Microsoft Teams AI Bot

Portfolio project that demonstrates how to build a conversational AI assistant for Microsoft Teams using Python and the Microsoft/Azure ecosystem.

The bot receives questions from Microsoft Teams through Microsoft Bot Framework, retrieves optional context from Azure AI Search, generates an answer with Azure OpenAI, and exposes REST endpoints that can also be deployed as Azure Functions.

## Why this project

This prototype is focused on a realistic enterprise use case: an internal support assistant that can answer operational questions, summarize information and automate simple requests inside Microsoft Teams.

## Stack

- Python
- Microsoft Bot Framework
- Microsoft Teams
- Azure OpenAI Service
- Azure AI Search
- Azure Functions
- Microsoft Graph API
- REST APIs
- Docker
- Git
- Prompt Engineering
- RAG architecture

## Architecture

```text
Microsoft Teams
      |
      v
Microsoft Bot Framework
      |
      v
Python Bot / REST API
      |
      +------> Azure AI Search (optional RAG context)
      |
      +------> Azure OpenAI Service
      |
      +------> Microsoft Graph API (optional M365 data)
      |
      v
Response to Teams
```

## Main features

- Conversational bot endpoint compatible with Microsoft Bot Framework.
- Azure OpenAI integration for generative responses.
- Prompt engineering with explicit enterprise/security instructions.
- Optional RAG retrieval with Azure AI Search.
- Optional Microsoft Graph API helper for Microsoft 365 integrations.
- REST endpoint (`/api/ask`) for testing without Teams.
- Azure Functions HTTP example for serverless deployment.
- Dockerfile for containerized execution.
- Local demo mode when Azure credentials are not configured.

## Project structure

```text
microsoft-teams-ai-bot/
├── app.py
├── ai_service.py
├── rag_service.py
├── graph_service.py
├── function_app.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── .gitignore
├── sample_request.json
└── teams-manifest/
    └── manifest.template.json
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

The local API runs on port `3978`.

### Health check

```bash
curl http://localhost:3978/health
```

### Test the AI REST endpoint

```bash
curl -X POST http://localhost:3978/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How do I report a phishing email?"}'
```

## Azure OpenAI configuration

Create an Azure OpenAI deployment and configure:

```env
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=2024-10-21
```

If these variables are empty, the project works in local demo mode so the flow can be tested without cloud credentials.

## Microsoft Bot Framework / Teams

Configure a Microsoft Entra application / bot registration and set:

```env
MICROSOFT_APP_ID=
MICROSOFT_APP_PASSWORD=
```

The Bot Framework messaging endpoint is:

```text
https://YOUR-HOST/api/messages
```

A Teams manifest template is included in `teams-manifest/manifest.template.json`.

## Azure AI Search / RAG

Optional variables:

```env
AZURE_SEARCH_ENDPOINT=
AZURE_SEARCH_KEY=
AZURE_SEARCH_INDEX=knowledge
```

When configured, the bot retrieves relevant documents before calling the LLM and injects that context into the prompt. When it is not configured, a small local knowledge base is used for demonstration.

## Microsoft Graph API

The `graph_service.py` module shows application-authentication using MSAL and a simple Microsoft Graph user lookup. Permissions must be granted in Microsoft Entra ID before using Graph in a real tenant.

## Azure Functions

`function_app.py` exposes a minimal HTTP-triggered serverless endpoint using the same AI service. It can be deployed independently when a lightweight integration is preferred.

## Docker

```bash
docker build -t microsoft-teams-ai-bot .
docker run --env-file .env -p 3978:3978 microsoft-teams-ai-bot
```

## Security notes

- No secrets are stored in the repository.
- Use environment variables or Azure Key Vault in production.
- Apply least-privilege permissions to Microsoft Graph.
- Add authentication, rate limiting and logging before production use.
- Validate user input and data sources before enabling enterprise actions.

## Possible next steps

- Copilot Studio integration.
- Power Platform workflow actions.
- Adaptive Cards for Teams.
- Azure Key Vault.
- Azure Container Apps deployment.
- Entra ID SSO.
- Production RAG with document ingestion and citations.

## Portfolio value

This project demonstrates practical knowledge of Python, bots, Azure AI, Azure OpenAI, Microsoft Bot Framework, Microsoft Teams, REST APIs, Azure Functions, Microsoft Graph, prompt engineering, RAG and Docker in one small end-to-end prototype.
