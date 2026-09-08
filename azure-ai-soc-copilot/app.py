import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

load_dotenv()

REQUIRED_ENV_VARS = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_DEPLOYMENT",
]


def local_fallback(alert: dict) -> dict:
    """Small offline fallback so the demo can run without cloud credentials."""
    event = alert.get("event", "Unknown event")
    source_ip = alert.get("source_ip", "unknown")
    user = alert.get("user", "unknown")
    attempts = int(alert.get("attempts", 1) or 1)

    severity = "high" if attempts >= 10 else "medium" if attempts >= 5 else "low"
    return {
        "mode": "local-demo",
        "summary": f"{event} detected from {source_ip} against user {user}.",
        "severity": severity,
        "category": "authentication",
        "recommended_actions": [
            "Validate whether the source IP is expected.",
            "Review recent authentication attempts for the affected user.",
            "Escalate if activity is repeated or confirmed as malicious.",
        ],
    }


def analyze_with_azure(alert: dict) -> str:
    llm = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        temperature=0,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a cybersecurity SOC assistant. Analyze the alert and return a concise response in JSON with these keys: summary, severity, category, recommended_actions. Do not invent evidence that is not present in the alert.",
            ),
            ("human", "Alert:\n{alert}"),
        ]
    )

    chain = prompt | llm
    response = chain.invoke({"alert": json.dumps(alert, ensure_ascii=False, indent=2)})
    return response.content


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze a security alert with Azure OpenAI + LangChain."
    )
    parser.add_argument(
        "--file",
        default="examples/alert.json",
        help="Path to a JSON alert file.",
    )
    args = parser.parse_args()

    alert_path = Path(args.file)
    if not alert_path.exists():
        raise SystemExit(f"Alert file not found: {alert_path}")

    with alert_path.open("r", encoding="utf-8") as file:
        alert = json.load(file)

    missing = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]

    if missing:
        result = local_fallback(alert)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print("\nCloud mode disabled. Configure .env to use Azure OpenAI.")
        return

    print(analyze_with_azure(alert))


if __name__ == "__main__":
    main()
