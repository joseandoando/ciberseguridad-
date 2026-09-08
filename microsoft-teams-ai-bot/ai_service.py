import os
from typing import Optional

from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()


SYSTEM_PROMPT = """You are an enterprise AI assistant for Microsoft Teams.
Answer clearly and concisely. Use the provided context when available.
Do not invent internal policies, credentials, permissions or company data.
If the context is insufficient, say that more information is required.
For security-related questions, prefer safe and auditable recommendations.
"""


class AIService:
    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
        self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "").strip()
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

        self.client: Optional[AzureOpenAI] = None
        if self.endpoint and self.api_key and self.deployment:
            self.client = AzureOpenAI(
                azure_endpoint=self.endpoint,
                api_key=self.api_key,
                api_version=self.api_version,
            )

    async def answer(self, question: str, context: str = "") -> str:
        question = (question or "").strip()
        if not question:
            return "Please provide a question."

        if not self.client:
            context_hint = f" Context found: {context[:240]}" if context else ""
            return (
                "[DEMO MODE] I received your question: "
                f"'{question}'. Azure OpenAI credentials are not configured, so no cloud call was made."
                f"{context_hint}"
            )

        user_prompt = f"""Context:
{context or 'No external context was retrieved.'}

User question:
{question}

Return a concise enterprise-ready answer."""

        response = self.client.chat.completions.create(
            model=self.deployment,
            temperature=0.2,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content or "No response generated."
