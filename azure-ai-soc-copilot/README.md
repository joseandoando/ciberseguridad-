# Azure AI SOC Copilot

Simple Generative AI prototype that analyzes a cybersecurity alert and generates a concise summary, severity, category and recommended actions.

The project was built to demonstrate practical use of Python, LLM APIs, Azure OpenAI, LangChain, Git and Docker in a small real-world automation.

## Stack

- Python
- Azure OpenAI / Azure AI
- LangChain
- Docker
- Git
- JSON-based integrations

## How it works

1. Reads a security alert from JSON.
2. Builds a structured prompt with LangChain.
3. Sends the alert to an Azure OpenAI deployment.
4. Returns a concise SOC-oriented analysis.
5. If Azure credentials are not configured, it runs in local demo mode.

## Example input

```json
{
  "event": "Multiple failed SSH login attempts",
  "source_ip": "203.0.113.45",
  "destination_ip": "10.10.10.41",
  "user": "admin",
  "attempts": 14,
  "source": "wazuh"
}
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py --file examples/alert.json
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py --file examples/alert.json
```

## Azure configuration

Configure the following variables in `.env`:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your_deployment_name
AZURE_OPENAI_API_VERSION=2024-10-21
```

Never commit real API keys.

## Docker

```bash
docker build -t azure-ai-soc-copilot .
docker run --env-file .env azure-ai-soc-copilot
```

## Portfolio value

This prototype demonstrates:

- Consumption of Generative AI / LLM APIs
- Prompt construction with LangChain
- Python automation
- Azure cloud integration
- Docker containerization
- Git-based source control
- Application of Generative AI to a real operational use case

## Possible next steps

- REST API with FastAPI
- Web interface with Streamlit
- Azure Container Apps deployment
- Wazuh webhook integration
- Structured output validation with Pydantic
