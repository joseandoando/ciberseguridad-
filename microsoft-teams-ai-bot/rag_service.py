import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


LOCAL_KNOWLEDGE = [
    {
        "title": "Phishing reporting",
        "content": "Report suspicious email using the organization's security channel, preserve the message, avoid opening links or attachments, and provide sender, subject and timestamp.",
    },
    {
        "title": "Password reset",
        "content": "Use the approved identity portal or service desk workflow. Never share passwords or MFA codes through chat.",
    },
    {
        "title": "Access requests",
        "content": "Access should follow least privilege and require the appropriate business approval before provisioning.",
    },
]


class RAGService:
    def __init__(self) -> None:
        self.endpoint = os.getenv("AZURE_SEARCH_ENDPOINT", "").strip()
        self.key = os.getenv("AZURE_SEARCH_KEY", "").strip()
        self.index_name = os.getenv("AZURE_SEARCH_INDEX", "knowledge").strip()

    def retrieve(self, query: str, top: int = 3) -> str:
        if self.endpoint and self.key:
            try:
                from azure.core.credentials import AzureKeyCredential
                from azure.search.documents import SearchClient

                client = SearchClient(
                    endpoint=self.endpoint,
                    index_name=self.index_name,
                    credential=AzureKeyCredential(self.key),
                )
                results = client.search(search_text=query, top=top)
                chunks: List[str] = []
                for item in results:
                    title = item.get("title", "Document")
                    content = item.get("content", "")
                    chunks.append(f"{title}: {content}")
                return "\n".join(chunks)
            except Exception as exc:
                return f"Azure AI Search unavailable ({type(exc).__name__}). Using local demo knowledge.\n" + self._local_retrieve(query)

        return self._local_retrieve(query)

    def _local_retrieve(self, query: str) -> str:
        words = {word.lower().strip(".,?!") for word in query.split() if len(word) > 3}
        scored = []
        for item in LOCAL_KNOWLEDGE:
            haystack = f"{item['title']} {item['content']}".lower()
            score = sum(1 for word in words if word in haystack)
            scored.append((score, item))

        scored.sort(key=lambda value: value[0], reverse=True)
        selected = [item for score, item in scored[:2] if score > 0]
        if not selected:
            return ""

        return "\n".join(f"{item['title']}: {item['content']}" for item in selected)
