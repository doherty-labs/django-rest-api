import logging
import os

import requests

logger = logging.getLogger(__name__)


class HcpVaultSecrets:
    def __init__(
        self,
    ):
        self.client_id = os.environ.get("HCP_CLIENT_ID", "")
        self.client_secret = os.environ.get(
            "HCP_CLIENT_SECRET",
            "",
        )
        self.org_id = os.environ.get("HCP_ORG_ID", "")
        self.project_id = os.environ.get("HCP_PROJECT_ID", "")
        self.app_name = os.environ.get("HCP_APP_NAME", "")

    def get_token(self):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "audience": "https://api.hashicorp.cloud",
        }
        response = requests.post(
            "https://auth.idp.hashicorp.com/oauth2/token",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def get_secret(self) -> dict:
        token = self.get_token()
        headers = {
            "Authorization": "Bearer " + token,
        }

        url = f"https://api.cloud.hashicorp.com/secrets/2023-06-13/organizations/{self.org_id}/projects/{self.project_id}/apps/{self.app_name}/open"
        response = requests.get(
            url,
            headers=headers,
        )
        response.raise_for_status()
        secrets = response.json()["secrets"]
        results: dict = {}

        for secret in secrets:
            results[secret["name"]] = secret["version"]["value"]

        return results
