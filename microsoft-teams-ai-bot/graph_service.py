import os
from typing import Any, Dict, Optional

import msal
import requests
from dotenv import load_dotenv

load_dotenv()


class GraphService:
    """Minimal Microsoft Graph helper using app-only authentication.

    A real tenant must grant the required Microsoft Graph application permissions
    and administrator consent before these methods can access directory data.
    """

    def __init__(self) -> None:
        self.tenant_id = os.getenv("AZURE_TENANT_ID", "").strip()
        self.client_id = os.getenv("GRAPH_CLIENT_ID", "").strip()
        self.client_secret = os.getenv("GRAPH_CLIENT_SECRET", "").strip()
        self.scope = ["https://graph.microsoft.com/.default"]

    def _token(self) -> Optional[str]:
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            return None

        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            client_credential=self.client_secret,
        )
        result = app.acquire_token_for_client(scopes=self.scope)
        return result.get("access_token")

    def get_user_by_email(self, email: str) -> Dict[str, Any]:
        token = self._token()
        if not token:
            return {
                "demo": True,
                "message": "Microsoft Graph credentials are not configured.",
                "requested_email": email,
            }

        response = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{email}",
            headers={"Authorization": f"Bearer {token}"},
            params={"$select": "displayName,mail,userPrincipalName,jobTitle"},
            timeout=15,
        )
        response.raise_for_status()
        return response.json()
